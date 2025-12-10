# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

from db.crud import fetch, update, lock_rows
from db import conn
from db.tx import transaction

def db_fetch_pending_orders(store_id):
    """查詢門市的待處理訂單
    
    Args:
        store_id: 門市 ID
    
    Returns:
        list: 待處理訂單列表
    """
    sql = """
        SELECT o.order_id, o.user_id, o.order_type, o.placed_at, o.total_price
        FROM ORDERS o
        WHERE o.store_id = %s AND o.order_status = 'placed'
        ORDER BY o.placed_at ASC
    """
    conn.cur.execute(sql, (store_id,))
    rows = conn.cur.fetchall()
    
    return [
        {
            "order_id": row[0],
            "user_id": row[1],
            "order_type": row[2],
            "placed_at": row[3],
            "total_price": row[4],
        }
        for row in rows
    ]


def db_fetch_accepted_orders(store_id):
    """查詢門市的已接受訂單（進行中）
    
    Args:
        store_id: 門市 ID
    
    Returns:
        list: 已接受訂單列表
    """
    sql = """
        SELECT o.order_id, o.user_id, o.order_type, o.placed_at, o.accepted_at, o.total_price
        FROM ORDERS o
        WHERE o.store_id = %s AND o.order_status = 'accepted'
        ORDER BY o.accepted_at ASC
    """
    conn.cur.execute(sql, (store_id,))
    rows = conn.cur.fetchall()
    
    return [
        {
            "order_id": row[0],
            "user_id": row[1],
            "order_type": row[2],
            "placed_at": row[3],
            "accepted_at": row[4],
            "total_price": row[5],
        }
        for row in rows
    ]


def db_fetch_history_orders(store_id):
    """查詢門市的歷史訂單（已完成/已拒絕）
    
    Args:
        store_id: 門市 ID
    
    Returns:
        list: 歷史訂單列表
    """
    sql = """
        SELECT o.order_id, o.user_id, o.order_type, o.order_status, 
               o.placed_at, o.completed_at, o.rejected_reason, o.total_price
        FROM ORDERS o
        WHERE o.store_id = %s 
          AND o.order_status IN ('completed', 'rejected', 'cancelled')
        ORDER BY COALESCE(o.completed_at, o.placed_at) DESC
        LIMIT 50
    """
    conn.cur.execute(sql, (store_id,))
    rows = conn.cur.fetchall()
    
    return [
        {
            "order_id": row[0],
            "user_id": row[1],
            "order_type": row[2],
            "order_status": row[3],
            "placed_at": row[4],
            "completed_at": row[5],
            "rejected_reason": row[6],
            "total_price": row[7],
        }
        for row in rows
    ]

def db_accept_order(order_id):
    """接受訂單（僅限待處理狀態）
    
    Args:
        order_id: 訂單 ID
    
    Returns:
        tuple: 更新後的訂單記錄
        
    Raises:
        ValueError: 訂單不存在或狀態不正確
    """
    # ✅ 修正 Race Condition: 在 WHERE 條件中檢查狀態，確保原子性
    with transaction():
        # Lock the order row for update
        locked = lock_rows("ORDERS", ["order_status"], {"order_id": order_id})
        if not locked:
            raise ValueError("Order not found")
        status = locked[0][0]
        if status != "placed":
            raise ValueError("Order cannot be accepted: current status is not 'placed'")
        # Update order to accepted
        update("ORDERS", {"order_status": "accepted", "accepted_at": "CURRENT_TIMESTAMP"}, {"order_id": order_id})
        row = conn.cur.fetchone()
        if not row:
            raise RuntimeError("Failed to accept order")
        return row

def db_reject_order(order_id, rejected_reason):
    with transaction():
        # Lock the order row for update
        locked = lock_rows("ORDERS", ["order_status"], {"order_id": order_id})
        if not locked:
            raise ValueError("Order not found")
        status = locked[0][0]
        if status != "placed":
            raise ValueError("Order cannot be rejected: current status is not 'placed'")
        # Update order to rejected with reason
        sql = """
            UPDATE ORDERS
            SET order_status = 'rejected', rejected_at = CURRENT_TIMESTAMP, rejected_reason = %s
            WHERE order_id = %s
            RETURNING *
        """
        conn.cur.execute(sql, (rejected_reason, order_id))
        row = conn.cur.fetchone()
        if not row:
            raise RuntimeError("Failed to reject order")
        return row


def db_complete_order(order_id):
    """完成訂單（僅限已接受狀態）
    
    Args:
        order_id: 訂單 ID
    
    Returns:
        tuple: 更新後的訂單記錄
        
    Raises:
        ValueError: 訂單不存在或狀態不正確
    """
    # ✅ 修正 Race Condition: 在 WHERE 條件中檢查狀態，確保原子性
    with transaction():
        # Lock order for update
        locked = lock_rows("ORDERS", ["order_status"], {"order_id": order_id})
        if not locked:
            raise ValueError("Order not found")
        status = locked[0][0]
        if status != "accepted":
            raise ValueError("Order cannot be completed: status is not 'accepted'")
        sql = """
            UPDATE ORDERS
            SET order_status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE order_id = %s AND order_status = 'accepted'
            RETURNING *
        """
        conn.cur.execute(sql, (order_id,))
        row = conn.cur.fetchone()
    
        if not row:
            # 查詢訂單是否存在及當前狀態
            conn.cur.execute("SELECT order_status FROM ORDERS WHERE order_id = %s", (order_id,))
            result = conn.cur.fetchone()
            if not result:
                raise ValueError(f"訂單 {order_id} 不存在")
            else:
                raise ValueError(f"訂單狀態為「{result[0]}」，無法完成（只能完成已接受訂單）")
    
        conn.commit()
        return row


def db_cancel_order(order_id, user_id):
    """取消訂單（僅限待處理狀態）
    
    Args:
        order_id: 訂單 ID
        user_id: 使用者 ID（用於驗證訂單所有權）
    
    Returns:
        tuple: 更新後的訂單記錄
        
    Raises:
        ValueError: 訂單不存在、不屬於該使用者或狀態不正確
    """
    # ✅ 修正 Race Condition: 使用原子性的 UPDATE，在 WHERE 條件中同時檢查
    with transaction():
        # Lock order for update
        locked = lock_rows("ORDERS", ["order_status", "user_id"], {"order_id": order_id, "user_id": user_id})
        if not locked:
            raise ValueError("Order not found or does not belong to user")
        status = locked[0][0]
        if status != "placed":
            raise ValueError("Order cannot be cancelled: status is not 'placed'")
        sql_update = """
            UPDATE ORDERS
            SET order_status = 'cancelled'
            WHERE order_id = %s AND user_id = %s AND order_status = 'placed'
            RETURNING *
        """
        conn.cur.execute(sql_update, (order_id, user_id))
        row = conn.cur.fetchone()
    
        if not row:
            # 查詢失敗原因：訂單不存在 or 不屬於該使用者 or 狀態不對
            conn.cur.execute(
                "SELECT order_status FROM ORDERS WHERE order_id = %s AND user_id = %s", 
                (order_id, user_id)
            )
            result = conn.cur.fetchone()
        
            if not result:
                raise ValueError("訂單不存在或不屬於您")
            else:
                raise ValueError(f"訂單狀態為「{result[0]}」，無法取消（只能取消待處理訂單）")
    
        conn.commit()
        return row


def db_fetch_user_orders(user_id):
    """查詢使用者的所有訂單
    
    Args:
        user_id: 使用者 ID
    
    Returns:
        list: 訂單列表
    """
    conditions = {"user_id": user_id}
    rows = fetch("ORDERS", conditions, order_by="placed_at DESC")
    
    # ORDERS 表欄位順序：
    # 0:order_id, 1:user_id, 2:store_id, 3:order_status, 4:order_type,
    # 5:delivery_address, 6:receiver_name, 7:receiver_phone, 8:placed_at,
    # 9:accepted_at, 10:completed_at, 11:rejected_reason, 12:total_price,
    # 13:payment_status, 14:payment_method
    
    return [
        {
            "order_id": row[0],
            "store_id": row[2],
            "order_status": row[3],
            "order_type": row[4],
            "placed_at": row[8],
            "total_price": row[12],
        }
        for row in rows
    ]
