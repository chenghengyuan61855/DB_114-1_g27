# db/rating/fetch.py
from db.crud import fetch, selective_fetch
from db import conn


def db_fetch_brand_ratings(brand_id):
    """查詢品牌下所有商品的評價"""
    sql = """
        SELECT 
            oir.order_item_id,
            oir.order_item_rating,
            oir.order_item_comment,
            oir.created_at,
            oi.product_id,
            p.product_name,
            oi.order_id,
            o.store_id,
            s.store_name
        FROM ORDER_ITEM_RATING oir
        JOIN ORDER_ITEM oi ON oir.order_item_id = oi.order_item_id
        JOIN PRODUCT p ON oi.product_id = p.product_id
        JOIN ORDERS o ON oi.order_id = o.order_id
        JOIN STORE s ON o.store_id = s.store_id
        WHERE p.brand_id = %s
        ORDER BY oir.created_at DESC
    """
    
    conn.cur.execute(sql, (brand_id,))
    rows = conn.cur.fetchall()
    
    return [
        {
            "order_item_id": row[0],
            "rating": row[1],
            "comment": row[2],
            "created_at": row[3],
            "product_id": row[4],
            "product_name": row[5],
            "order_id": row[6],
            "store_id": row[7],
            "store_name": row[8],
        }
        for row in rows
    ]


def db_fetch_product_ratings(product_id):
    """查詢特定商品的所有評價"""
    sql = """
        SELECT 
            oir.order_item_id,
            oir.order_item_rating,
            oir.order_item_comment,
            oir.created_at,
            oi.product_id,
            oi.order_id,
            o.user_id,
            o.store_id,
            o.completed_at
        FROM ORDER_ITEM_RATING oir
        JOIN ORDER_ITEM oi ON oir.order_item_id = oi.order_item_id
        JOIN ORDERS o ON oi.order_id = o.order_id
        WHERE oi.product_id = %s
        ORDER BY oir.created_at DESC
    """
    
    conn.cur.execute(sql, (product_id,))
    rows = conn.cur.fetchall()
    
    return [
        {
            "order_item_id": row[0],
            "rating": row[1],
            "comment": row[2],
            "created_at": row[3],
            "product_id": row[4],
            "order_id": row[5],
            "user_id": row[6],
            "store_id": row[7],
            "completed_at": row[8],
        }
        for row in rows
    ]


def db_fetch_low_rated_products(brand_id, threshold=3):
    """查詢低評分商品"""
    sql = """
        SELECT 
            p.product_id,
            p.product_name,
            COUNT(oir.order_item_rating) as rating_count,
            AVG(oir.order_item_rating) as avg_rating,
            MIN(oir.order_item_rating) as min_rating,
            MAX(oir.order_item_rating) as max_rating
        FROM PRODUCT p
        JOIN ORDER_ITEM oi ON p.product_id = oi.product_id
        JOIN ORDER_ITEM_RATING oir ON oi.order_item_id = oir.order_item_id
        WHERE p.brand_id = %s
        GROUP BY p.product_id, p.product_name
        HAVING AVG(oir.order_item_rating) < %s
        ORDER BY avg_rating ASC
    """
    
    conn.cur.execute(sql, (brand_id, threshold))
    rows = conn.cur.fetchall()
    
    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "rating_count": row[2],
            "avg_rating": float(row[3]) if row[3] else 0,
            "min_rating": row[4],
            "max_rating": row[5],
        }
        for row in rows
    ]


def db_fetch_rating_statistics(brand_id):
    """查詢品牌的評價統計"""
    sql = """
        SELECT 
            COUNT(DISTINCT oi.product_id) as total_products,
            COUNT(oir.order_item_rating) as total_ratings,
            AVG(oir.order_item_rating) as overall_avg_rating,
            COUNT(CASE WHEN oir.order_item_rating = 5 THEN 1 END) as five_star,
            COUNT(CASE WHEN oir.order_item_rating = 4 THEN 1 END) as four_star,
            COUNT(CASE WHEN oir.order_item_rating = 3 THEN 1 END) as three_star,
            COUNT(CASE WHEN oir.order_item_rating = 2 THEN 1 END) as two_star,
            COUNT(CASE WHEN oir.order_item_rating = 1 THEN 1 END) as one_star
        FROM ORDER_ITEM_RATING oir
        JOIN ORDER_ITEM oi ON oir.order_item_id = oi.order_item_id
        JOIN PRODUCT p ON oi.product_id = p.product_id
        WHERE p.brand_id = %s
    """
    
    conn.cur.execute(sql, (brand_id,))
    row = conn.cur.fetchone()
    
    if not row:
        return None
    
    return {
        "total_products": row[0],
        "total_ratings": row[1],
        "overall_avg_rating": float(row[2]) if row[2] else 0,
        "five_star": row[3],
        "four_star": row[4],
        "three_star": row[5],
        "two_star": row[6],
        "one_star": row[7],
    }


def db_fetch_top_rated_products(brand_id, limit=10):
    """查詢高評分商品"""
    sql = """
        SELECT 
            p.product_id,
            p.product_name,
            COUNT(oir.order_item_rating) as rating_count,
            AVG(oir.order_item_rating) as avg_rating
        FROM PRODUCT p
        JOIN ORDER_ITEM oi ON p.product_id = oi.product_id
        JOIN ORDER_ITEM_RATING oir ON oi.order_item_id = oir.order_item_id
        WHERE p.brand_id = %s
        GROUP BY p.product_id, p.product_name
        HAVING COUNT(oir.order_item_rating) >= 5
        ORDER BY avg_rating DESC, rating_count DESC
        LIMIT %s
    """
    
    conn.cur.execute(sql, (brand_id, limit))
    rows = conn.cur.fetchall()
    
    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "rating_count": row[2],
            "avg_rating": float(row[3]) if row[3] else 0,
        }
        for row in rows
    ]
