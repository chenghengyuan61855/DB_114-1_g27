from db.crud import insert

def insert_order_rating(order_id, rating, comment):
    """插入訂單評分到 ORDER_RATING 表"""
    data = {
        "order_id": order_id,
        "order_rating": rating,  # ← 修改：rating → order_rating
        "order_comment": comment  # ← 修改：comment → order_comment
    }
    insert("ORDER_RATING", data)

def insert_order_item_rating(order_item_id, rating, comment):
    """插入訂單項目評分到 ORDER_ITEM_RATING 表"""
    data = {
        "order_item_id": order_item_id,
        "order_item_rating": rating,  # ← 修改：rating → order_item_rating
        "order_item_comment": comment  # ← 修改：comment → order_item_comment
    }
    insert("ORDER_ITEM_RATING", data)