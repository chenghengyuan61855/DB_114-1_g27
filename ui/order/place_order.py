from ui.helper import cancel_check
from ui.order.select_brand import ui_select_brand
from ui.order.select_store import ui_select_store
from ui.order.select_type import ui_select_order_type
from db.product.fetch import db_fetch_product, db_fetch_store_product, db_fetch_product_categories

def ui_place_order():
    print("\n=== Place Order ===")
    print("(Type ':q' in any input to cancel order placement)")
    print("(Type ':b' in any input to go back to last step)\n")

    step = 0
    order_type = None
    brand_id = None
    store_id = None

    while True:
        if step == 0:
            order_type = ui_select_order_type()
            if order_type is None: return         # Cancel
            if order_type == ":b": continue       # No previous step, ignore
            step += 1

        if step == 1:
            brand_id = ui_select_brand()
            if brand_id is None: return           # Cancel
            if brand_id == ":b":
                step -= 1
                continue
            step += 1

        if step == 2:
            store_id = ui_select_store(order_type, brand_id)
            if store_id is None: return           # Cancel
            if store_id == ":b":
                step -= 1
                continue
            step += 1

        if step == 3:
            break
    # Continue with placing order using order_type, brand_id, store_id ...
    


    
        
        
        