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
    print("Available Stores:\n")
    NAME_WIDTH = 10      # 店名欄位寬度
    ADDR_WIDTH = 30      # 地址欄位寬度

    for store in stores:
        index = store[0]
        name = store[2]
        addr = store[3]
        phone = store[4]

        print(f"{index}. {name:<{NAME_WIDTH}} （電話：{phone}　地址：{addr}）")
    
    return stores  # ← 加上這一行



def select_store_from_user(available_stores):
    """讓用戶輸入門市 ID"""
    while True:
        store_id = input("\nEnter Store ID to select a store: ").strip()
        
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