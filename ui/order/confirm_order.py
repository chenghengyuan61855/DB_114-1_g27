# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-07
# ============================

from db.order.place import db_place_order_pickup, db_place_order_delivery
from ui.helper import cancel_check, clear_screen

def ui_confirm_and_submit_order(user_id, store_id, order_type, selected_items):
    """確認並送出訂單"""
    clear_screen()
    
    print("\n=== Order Summary ===")
    print(f"Store ID: {store_id}")
    print(f"Order Type: {order_type}")
    print("\nItems:")
    
    total_price = 0
    for idx, item in enumerate(selected_items, 1):
        print(f"\n{idx}. {item['product_name']} x {item['quantity']}")
        print(f"   Unit Price: ${item['unit_price']}")
        print(f"   Options: {item['customization']}")
        print(f"   Option Price: ${item['option_price']}")
        print(f"   Subtotal: ${item['subtotal']}")
        total_price += item['subtotal']
    
    print(f"\n{'='*40}")
    print(f"Total Price: ${total_price}")
    print(f"{'='*40}\n")
    
    # 確認訂單
    confirm = input("Confirm order? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Order cancelled")
        return
    
    # 付款方式
    print("\nPayment Method:")
    print("1. Cash")
    print("2. Card")
    print("3. Online")
    
    while True:
        payment_choice = input("Select payment method (1-3): ").strip()
        if cancel_check(payment_choice, "Order Placement"):
            return
        
        if payment_choice == '1':
            payment_method = 'cash'
            break
        elif payment_choice == '2':
            payment_method = 'card'
            break
        elif payment_choice == '3':
            payment_method = 'online'
            break
        else:
            print("❌ Invalid choice")
    
    payment_status = 'unpaid'  # 預設未付款
    
    try:
        if order_type.lower() == 'pickup':
            # 自取訂單
            order_id = db_place_order_pickup(
                user_id, 
                store_id, 
                total_price, 
                payment_method, 
                payment_status
            )
        else:
            # 外送訂單（需要額外資訊）
            print("\n=== Delivery Information ===")
            
            delivery_address = input("Delivery Address: ").strip()
            if cancel_check(delivery_address, "Order Placement"):
                return
            
            receiver_name = input("Receiver Name: ").strip()
            if cancel_check(receiver_name, "Order Placement"):
                return
            
            receiver_phone = input("Receiver Phone: ").strip()
            if cancel_check(receiver_phone, "Order Placement"):
                return
            
            order_id = db_place_order_delivery(
                user_id,
                store_id,
                total_price,
                payment_method,
                payment_status,
                delivery_address,
                receiver_name,
                receiver_phone
            )
        
        print(f"\n✅ Order placed successfully!")
        print(f"Order ID: {order_id}")
        print(f"Total: ${total_price}")
        
        # TODO: 插入 ORDER_ITEM 和 ORDER_ITEM_OPTION（需要實作）
        
    except Exception as e:
        print(f"❌ Error placing order: {e}")