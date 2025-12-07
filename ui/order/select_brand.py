from db.crud import fetch
from ui.helper import cancel_check

def ui_show_brand_list():
    brands = fetch("BRAND", {"is_active": True}, order_by="brand_id")
    if not brands:
        print("No active brands available.")
        return []
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
        
        if brand_id not in [str(brand[0]) for brand in available_brands]:
            print("Invalid Brand ID. Please try again.")
            continue
        
        return int(brand_id)
    