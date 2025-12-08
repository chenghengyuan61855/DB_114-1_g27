# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.order.place import (
    db_place_order_pickup, 
    db_place_order_delivery,
    db_insert_order_item,
    db_insert_order_item_option
)
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
        
        # ✅ 修正：從 tuple 中提取 order_id（第一個元素）
        actual_order_id = order_id[0] if isinstance(order_id, tuple) else order_id
        
        print(f"\n✅ Order placed successfully!")
        print(f"Order ID: {actual_order_id}")
        print(f"Total: ${total_price}")
        
        # ✅ 插入訂單明細和選項
        for item in selected_items:
            # 插入 ORDER_ITEM
            order_item_result = db_insert_order_item(
                order_id=actual_order_id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                option_total_adjust=item.get('option_price', 0)  # ✅ 新增：選項總調整價格
            )
            
            # ✅ 修正：從 tuple 中提取 order_item_id（第一個元素）
            actual_order_item_id = order_item_result[0] if isinstance(order_item_result, tuple) else order_item_result
            
            # 插入 ORDER_ITEM_OPTION（如果有選項）
            if 'selected_options' in item and item['selected_options']:
                for option_id in item['selected_options']:
                    db_insert_order_item_option(
                        order_item_id=actual_order_item_id,
                        option_id=option_id
                    )
        
        print("✅ Order items and options saved successfully!")
        
    except Exception as e:
        print(f"❌ Error placing order: {e}")