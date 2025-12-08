from datetime import datetime
from db.nosql import drink_clicks

def log_drink_click(user_id, brand_id, product_id):
    data = {
        "user_id": user_id,
        "brand_id": brand_id,
        "product_id": product_id,
        "timestamp": datetime.now(),
        "submitted": False
    }
    drink_clicks.insert_one(data)
