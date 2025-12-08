from db.crud import insert, selective_fetch

def insert_order_rating(order_id, rating, comment):
    """插入訂單評分到 ORDER_RATING 表"""
    data = {
        "order_id": order_id,
        "rating": rating,
        "comment": comment
    }
    insert("ORDER_RATING", data)