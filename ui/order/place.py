from ui.helper import cancel_check
from db.order.place import db_place_order_pickup, db_place_order_delivery

def ui_place_order(user_id, store_id):
    print("\n=== Place Order ===")
    print("Select order type:")
    print("1. Pickup")
    print("2. Delivery")
    
    while True:
        order_type = input("Enter choice (1 or 2): ").strip()
        if cancel_check(order_type, "Order Placement"):
            return None
        
        if order_type not in ['1', '2']:
            print("❌ Invalid choice. Please enter 1 or 2.")
            continue
        break

    total_price = float(input("Enter total price: "))
    payment_method = input("Enter payment method (e.g., credit card, cash): ")
    payment_status = input("Enter payment status (e.g., paid, unpaid): ")

    if order_type == '1':
        order_id = db_place_order_pickup(user_id, store_id, total_price, payment_method, payment_status)
    else:
        delivery_address = input("Enter delivery address: ")
        reciver_name = input("Enter receiver name: ")
        reciver_phone = input("Enter receiver phone: ")
        order_id = db_place_order_delivery(user_id, store_id, total_price, payment_method, payment_status,
                                           delivery_address, reciver_name, reciver_phone)
    
    print(f"✅ Order placed successfully! Order ID: {order_id}")
    return order_id