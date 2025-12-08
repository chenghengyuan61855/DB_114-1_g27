# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

from db.crud import fetch, update
from db import conn

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
    """接受訂單
    
    Args:
        order_id: 訂單 ID
    
    Returns:
        tuple: 更新後的訂單記錄
    """
    # 使用 SQL 直接更新以支持 CURRENT_TIMESTAMP
    sql = """
        UPDATE ORDERS
        SET order_status = 'accepted', accepted_at = CURRENT_TIMESTAMP
        WHERE order_id = %s
        RETURNING *
    """
    conn.cur.execute(sql, (order_id,))
    row = conn.cur.fetchone()
    conn.commit()  # ✅ 修正：connection.commit() → commit()
    return row


def db_reject_order(order_id, rejected_reason):
    """拒絕訂單
    
    Args:
        order_id: 訂單 ID
        rejected_reason: 拒絕原因
    
    Returns:
        tuple: 更新後的訂單記錄
    """
    row = update(
        "ORDERS",
        {
            "order_status": "rejected",
            "rejected_reason": rejected_reason
        },
        {"order_id": order_id}
    )
    return row


def db_complete_order(order_id):
    """完成訂單
    
    Args:
        order_id: 訂單 ID
    
    Returns:
        tuple: 更新後的訂單記錄
    """
    # 使用 SQL 直接更新以支持 CURRENT_TIMESTAMP
    sql = """
        UPDATE ORDERS
        SET order_status = 'completed', completed_at = CURRENT_TIMESTAMP
        WHERE order_id = %s
        RETURNING *
    """
    conn.cur.execute(sql, (order_id,))
    row = conn.cur.fetchone()
    conn.commit()  # ✅ 修正：connection.commit() → commit()
    return row


def db_cancel_order(order_id, user_id):
    """取消訂單（僅限待處理狀態）
    
    Args:
        order_id: 訂單 ID
        user_id: 使用者 ID（用於驗證訂單所有權）
    
    Returns:
        tuple: 更新後的訂單記錄，若失敗則返回 None
    """
    # 先檢查訂單是否屬於該使用者且狀態為 'placed'
    sql_check = """
        SELECT order_status FROM ORDERS
        WHERE order_id = %s AND user_id = %s
    """
    conn.cur.execute(sql_check, (order_id, user_id))
    result = conn.cur.fetchone()
    
    if not result:
        raise ValueError("訂單不存在或不屬於您")
    
    if result[0] != 'placed':
        raise ValueError(f"訂單狀態為「{result[0]}」，無法取消")
    
    # 更新訂單狀態為 cancelled
    sql_update = """
        UPDATE ORDERS
        SET order_status = 'cancelled'
        WHERE order_id = %s
        RETURNING *
    """
    conn.cur.execute(sql_update, (order_id,))
    row = conn.cur.fetchone()
    conn.commit()  # ✅ 修正：connection.commit() → commit()
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
