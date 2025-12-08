# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-08
# ASSISTED BY: Claude
# PURPOSE: 評分系統的建立功能（防止重複評分）
# ============================

from db import conn

def db_create_order_rating(order_id, order_rating, order_comment=None):
    """建立訂單評分（防止重複評分）
    
    Args:
        order_id: 訂單 ID
        order_rating: 評分（1-5）
        order_comment: 評論內容（可選）
    
    Returns:
        tuple: 新增或更新後的評分記錄
        
    Raises:
        ValueError: 訂單不存在或評分不在有效範圍
        psycopg2.Error: 資料庫錯誤
    """
    # 驗證評分範圍
    if not (1 <= order_rating <= 5):
        raise ValueError("評分必須介於 1 到 5 之間")
    
    # ✅ 使用 INSERT ... ON CONFLICT 防止重複評分
    # 如果 order_id 已存在，則更新評分；否則新增
    sql = """
        INSERT INTO ORDER_RATING (order_id, order_rating, order_comment)
        VALUES (%s, %s, %s)
        ON CONFLICT (order_id) 
        DO UPDATE SET 
            order_rating = EXCLUDED.order_rating,
            order_comment = EXCLUDED.order_comment,
            created_at = CURRENT_TIMESTAMP
        RETURNING *
    """
    
    conn.cur.execute(sql, (order_id, order_rating, order_comment))
    row = conn.cur.fetchone()
    conn.commit()
    
    return row


def db_create_order_rating_strict(order_id, order_rating, order_comment=None):
    """建立訂單評分（嚴格模式：不允許重複評分）
    
    與 db_create_order_rating 不同，此函數會在訂單已被評分時拋出例外
    
    Args:
        order_id: 訂單 ID
        order_rating: 評分（1-5）
        order_comment: 評論內容（可選）
    
    Returns:
        tuple: 新增的評分記錄
        
    Raises:
        ValueError: 訂單已被評分、訂單不存在或評分不在有效範圍
        psycopg2.Error: 資料庫錯誤
    """
    # 驗證評分範圍
    if not (1 <= order_rating <= 5):
        raise ValueError("評分必須介於 1 到 5 之間")
    
    # ✅ 先檢查是否已經評分
    check_sql = "SELECT order_id FROM ORDER_RATING WHERE order_id = %s"
    conn.cur.execute(check_sql, (order_id,))
    existing = conn.cur.fetchone()
    
    if existing:
        raise ValueError(f"訂單 {order_id} 已經被評分，無法重複評分")
    
    # 驗證訂單是否存在且已完成
    order_check_sql = """
        SELECT order_status FROM ORDERS 
        WHERE order_id = %s
    """
    conn.cur.execute(order_check_sql, (order_id,))
    order = conn.cur.fetchone()
    
    if not order:
        raise ValueError(f"訂單 {order_id} 不存在")
    
    if order[0] != 'completed':
        raise ValueError(f"訂單狀態為「{order[0]}」，只能評分已完成的訂單")
    
    # 新增評分
    insert_sql = """
        INSERT INTO ORDER_RATING (order_id, order_rating, order_comment)
        VALUES (%s, %s, %s)
        RETURNING *
    """
    
    conn.cur.execute(insert_sql, (order_id, order_rating, order_comment))
    row = conn.cur.fetchone()
    conn.commit()
    
    return row


def db_create_order_item_rating(order_item_id, order_item_rating, order_item_comment=None):
    """建立訂單項目評分（防止重複評分）
    
    Args:
        order_item_id: 訂單項目 ID
        order_item_rating: 評分（1-5）
        order_item_comment: 評論內容（可選）
    
    Returns:
        tuple: 新增或更新後的評分記錄
        
    Raises:
        ValueError: 訂單項目不存在或評分不在有效範圍
        psycopg2.Error: 資料庫錯誤
    """
    # 驗證評分範圍
    if not (1 <= order_item_rating <= 5):
        raise ValueError("評分必須介於 1 到 5 之間")
    
    # ✅ 使用 INSERT ... ON CONFLICT 防止重複評分
    sql = """
        INSERT INTO ORDER_ITEM_RATING (order_item_id, order_item_rating, order_item_comment)
        VALUES (%s, %s, %s)
        ON CONFLICT (order_item_id) 
        DO UPDATE SET 
            order_item_rating = EXCLUDED.order_item_rating,
            order_item_comment = EXCLUDED.order_item_comment,
            created_at = CURRENT_TIMESTAMP
        RETURNING *
    """
    
    conn.cur.execute(sql, (order_item_id, order_item_rating, order_item_comment))
    row = conn.cur.fetchone()
    conn.commit()
    
    return row


def db_create_order_item_rating_strict(order_item_id, order_item_rating, order_item_comment=None):
    """建立訂單項目評分（嚴格模式：不允許重複評分）
    
    Args:
        order_item_id: 訂單項目 ID
        order_item_rating: 評分（1-5）
        order_item_comment: 評論內容（可選）
    
    Returns:
        tuple: 新增的評分記錄
        
    Raises:
        ValueError: 訂單項目已被評分或評分不在有效範圍
        psycopg2.Error: 資料庫錯誤
    """
    # 驗證評分範圍
    if not (1 <= order_item_rating <= 5):
        raise ValueError("評分必須介於 1 到 5 之間")
    
    # ✅ 先檢查是否已經評分
    check_sql = "SELECT order_item_id FROM ORDER_ITEM_RATING WHERE order_item_id = %s"
    conn.cur.execute(check_sql, (order_item_id,))
    existing = conn.cur.fetchone()
    
    if existing:
        raise ValueError(f"訂單項目 {order_item_id} 已經被評分，無法重複評分")
    
    # 新增評分
    insert_sql = """
        INSERT INTO ORDER_ITEM_RATING (order_item_id, order_item_rating, order_item_comment)
        VALUES (%s, %s, %s)
        RETURNING *
    """
    
    conn.cur.execute(insert_sql, (order_item_id, order_item_rating, order_item_comment))
    row = conn.cur.fetchone()
    conn.commit()
    
    return row
