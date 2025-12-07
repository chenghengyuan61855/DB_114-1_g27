from db.crud import fetch
from ui.order.select_brand import ui_select_brand
from ui.helper import cancel_check, clear_screen
from ui.order.helper import go_back_check

def ui_show_order_accepting_stores(order_type, brand_id=None):
    """顯示可接單的門市"""
    conditions = {"is_active": True}
    if brand_id:
        conditions["brand_id"] = brand_id
    
    if order_type == "delivery":
        conditions["accept_delivery"] = True
    
    stores = fetch("STORE", conditions, "store_id")
    
    if not stores:
        print("No stores available.")
        return []
    
    clear_screen()  # ← 新增：顯示門市列表前清屏
    print("\nAvailable Stores:")
    for store in stores:
        print(f"{store[0]}. {store[1]} - {store[2]} (Phone: {store[3]})")
    return stores


def select_store_from_user(available_stores):
    """讓用戶輸入門市 ID"""
    while True:
        store_id = input("Enter Store ID to select a store: ").strip()
        
        if cancel_check(store_id, "Order Placement"):
            return None
        
        if go_back_check(store_id):
            return ":b"
        
        if store_id not in [str(store[0]) for store in available_stores]:
            print("Invalid Store ID. Please try again.")
            continue
        
        return int(store_id)


def ui_select_store(order_type, brand_id):
    """選擇門市"""
    available_stores = ui_show_order_accepting_stores(order_type, brand_id)
    if not available_stores:
        return None
    
    return select_store_from_user(available_stores)