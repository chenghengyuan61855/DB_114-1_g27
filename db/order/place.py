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