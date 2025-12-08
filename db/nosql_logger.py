from datetime import datetime
from db.nosql import drink_clicks

def log_drink_click(user_id, brand_id, product_id):
    """記錄飲料點擊事件（使用者選擇了某個商品）
    
    注意：如果 MongoDB 未啟動，此函數會拋出異常，應該在調用處 catch
    """
    try:
        data = {
            "user_id": user_id,
            "brand_id": brand_id,
            "product_id": product_id,
            "timestamp": datetime.now(),
            "submitted": False,
            "order_id": None
        }
        drink_clicks.insert_one(data)
    except Exception:
        # 靜默失敗，不影響主流程
        pass


def mark_drink_as_submitted(user_id, brand_id, product_id, order_id):
    """標記飲料為「已送出訂單」"""
    drink_clicks.find_one_and_update(
        {
            "user_id": user_id,
            "brand_id": brand_id,
            "product_id": product_id,
            "submitted": False
        },
        {
            "$set": {
                "submitted": True,
                "order_id": order_id,
                "submitted_at": datetime.now()
            }
        },
        sort=[("timestamp", -1)]
    )
