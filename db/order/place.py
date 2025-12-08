from db.crud import fetch, update, insert

def db_place_order_pickup(user_id, store_id, total_price, payment_method, payment_status):

    order_data = {
        "user_id": user_id,
        "store_id": store_id,
        "order_status": "placed",
        "order_type": "pickup",
        "total_price": total_price,
        "payment_method": payment_method,
        "payment_status": payment_status,
    }

    order_id = insert("ORDERS", order_data)
    return order_id

def db_place_order_delivery(user_id, store_id, total_price, payment_method, payment_status,
                            delivery_address, receiver_name, receiver_phone):  # ✅ 修正：receiver_name, receiver_phone

    order_data = {
        "user_id": user_id,
        "store_id": store_id,
        "order_status": "placed",
        "order_type": "delivery",
        "delivery_address": delivery_address,
        "receiver_name": receiver_name,      # ✅ 修正：receiver_name
        "receiver_phone": receiver_phone,    # ✅ 修正：receiver_phone
        "total_price": total_price,
        "payment_method": payment_method,
        "payment_status": payment_status,
    }

    order_id = insert("ORDERS", order_data)
    return order_id


def db_insert_order_item(order_id, product_id, quantity, unit_price, option_total_adjust=0):
    """插入訂單明細
    
    Args:
        order_id: 訂單 ID
        product_id: 商品 ID
        quantity: 數量
        unit_price: 單價
        option_total_adjust: 選項總調整價格（預設為 0）
    
    Returns:
        int: 訂單明細 ID
    """
    # 計算該行總價：(商品單價 + 選項調整) * 數量
    line_total_price = (unit_price + option_total_adjust) * quantity
    
    order_item_data = {
        "order_id": order_id,
        "product_id": product_id,
        "qty": quantity,  # ✅ 修正：quantity → qty
        "unit_price": unit_price,
        "option_total_adjust": option_total_adjust,
        "line_total_price": line_total_price,
    }
    
    order_item_id = insert("ORDER_ITEM", order_item_data)
    return order_item_id


def db_insert_order_item_option(order_item_id, option_id):
    """插入訂單明細選項
    
    Args:
        order_item_id: 訂單明細 ID
        option_id: 選項 ID
    
    Returns:
        int: 插入的記錄 ID
    """
    order_item_option_data = {
        "order_item_id": order_item_id,
        "option_id": option_id,
    }
    
    # ORDER_ITEM_OPTION 沒有自動遞增的 ID，所以使用 insert 後不會返回 ID
    insert("ORDER_ITEM_OPTION", order_item_option_data)
    return True