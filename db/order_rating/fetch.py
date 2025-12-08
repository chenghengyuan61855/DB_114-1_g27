import db.conn as conn
import psycopg2

def check_order_rating_exists(order_id):
    """檢查訂單是否已經被評分
    
    Args:
        order_id: 訂單 ID
        
    Returns:
        bool: True 如果已評分，False 如果尚未評分
    """
    sql = """
        SELECT COUNT(*) 
        FROM ORDER_RATING 
        WHERE order_id = %s
    """
    conn.cur.execute(sql, (order_id,))
    count = conn.cur.fetchone()[0]
    return count > 0

def check_order_item_rating_exists(order_item_id):
    """檢查訂單項目是否已經被評分
    
    Args:
        order_item_id: 訂單項目 ID
        
    Returns:
        bool: True 如果已評分，False 如果尚未評分
    """
    sql = """
        SELECT COUNT(*) 
        FROM ORDER_ITEM_RATING 
        WHERE order_item_id = %s
    """
    conn.cur.execute(sql, (order_item_id,))
    count = conn.cur.fetchone()[0]
    return count > 0

def fetch_order_item_details(order_item_id):
    """
    Returns:
      - Main order item row (product with its UI display name, unit price, qty)
      - List of tuples: (option_name, price_adjust)
      - Final totals row: (option_total_price, line_total_price)
    """
    # Instead of relying on selective_fetch, do composite logic here:
    # You can use raw SQL, your ORM, or multi-fetches and data merging as needed.

    # 1. Fetch the main order item and joined product
    sql_main = """
        SELECT oi.order_item_id, 
               CONCAT(p.product_name, ' ', p.size) AS display_name,
               oi.unit_price, 
               oi.qty
        FROM ORDER_ITEM oi
        JOIN PRODUCT p ON oi.product_id = p.product_id
        WHERE oi.order_item_id = %s
        """
    
    conn.cur.execute(sql_main, (order_item_id,))
    main = conn.cur.fetchone()

    # 2. Fetch options (may be many)
    sql_options = """
        SELECT o.option_name, o.price_adjust
        FROM ORDER_ITEM_OPTION oio
        JOIN OPTION o ON oio.option_id = o.option_id
        WHERE oio.order_item_id = %s
        ORDER BY o.option_id
    """
    conn.cur.execute(sql_options, (order_item_id,))
    options = conn.cur.fetchall()
    if not options:
        options = []

    # 3. Fetch totals row
    sql_totals = """
        SELECT oi.option_total_adjust, oi.line_total_price
        FROM ORDER_ITEM oi
        WHERE oi.order_item_id = %s
    """
    conn.cur.execute(sql_totals, (order_item_id,))
    totals = conn.cur.fetchone()

    if not main or not totals:
        return None, None, None

    return main, options, totals