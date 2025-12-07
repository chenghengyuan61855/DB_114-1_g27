from ui.helper import cancel_check
from ui.order.select_brand import ui_select_brand
from ui.order.select_store import ui_show_order_accepting_stores
from ui.order.select_type import ui_select_order_type
from db.product.fetch import db_fetch_product, db_fetch_store_product, db_fetch_product_categories

def ui_place_order():
    print("\n=== Place Order ===")
    print("(Type ':q' in any input to cancel order placement)\n")

    brand_id = ui_select_brand()
    if not brand_id:
        return

    order_type = ui_select_order_type()
    if not order_type:
        return
    
    while True:
        available_stores = ui_show_order_accepting_stores(order_type, brand_id=int(brand_id))
        if not available_stores:
            print("No stores are currently accepting orders for the selected brand and order type.")
            while True:
                command = input("Select another brand (b), select another order type (o), quit (:q)? ").strip().lower()
                if command == 'b':
                    brand_id = ui_select_brand()
                    if not brand_id:
                        return
                    break
                elif command == 'o':
                    order_type = ui_select_order_type()
                    if not order_type:
                        return
                    break
                elif command == ':q':
                    print("Order placement cancelled.")
                    return
                else:
                    print("Invalid command. Please try again.")
            continue
        break
           


    
        
        
        