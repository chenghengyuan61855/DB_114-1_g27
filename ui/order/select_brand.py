from db.crud import selective_fetch
from ui.helper import cancel_check, clear_screen  # ← 新增 clear_screen
from ui.order.helper import go_back_check

def ui_show_brand_list():
    brands = selective_fetch("BRAND", ["brand_id", "brand_name"], {"is_active": True}, "brand_id")
    if not brands:
        print("No active brands available.")
        return []
    
    clear_screen()  # ← 顯示品牌列表前清屏
    print("\nAvailable Brands:")
    for brand in brands:
        print(f"{brand[0]}. {brand[1]}")
    return brands

def ui_select_brand():
    available_brands = ui_show_brand_list()
    if not available_brands:
        return None
    
    while True:
        brand_id = input("Enter Brand ID to select a brand: ").strip()

        if cancel_check(brand_id, "Order Placement"):
            return None
        
        if go_back_check(brand_id):
            return ":b"
        
        if brand_id not in [str(brand[0]) for brand in available_brands]:
            print("Invalid Brand ID. Please try again.")
            continue
        
        return int(brand_id)