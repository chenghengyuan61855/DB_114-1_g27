from ui.helper import cancel_check
from ui.order.show_brand import ui_show_brand_list
from ui.order.show_store import ui_show_order_accepting_stores, ui_show_delivery_accepting_stores
from ui.order.select_type import ui_select_order_type

def ui_place_order():
    print("\n=== Place Order ===")
    print("(Type ':q' in any input to cancel order placement)\n")

    available_brands = ui_show_brand_list()
    brand_id = input("Enter Brand ID to select a brand: ").strip()
    
    while True:
        if cancel_check(brand_id, "Order Placement"):
            return
        
        if brand_id not in available_brands:
            print("Invalid Brand ID. Please enter again.")

        break

    order_type = ui_select_order_type()

    if (order_type == "PICKUP"):
        stores = ui_show_order_accepting_stores(brand_id)

    elif (order_type == "DELIVERY"):
        stores = ui_show_delivery_accepting_stores(brand_id)

    else:
        print("An unexpected error occur.")
        return    

    
        
        
        