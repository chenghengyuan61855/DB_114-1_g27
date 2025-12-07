from ui.helper import cancel_check
from db.order.fetch import db_fetch_delivery_threshold
from ui.order.select_brand import ui_select_brand
from ui.order.select_store import ui_select_store
from ui.order.select_type import ui_select_order_type
from ui.order.select_items import ui_select_items

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
            order_item = ui_select_items(brand_id, store_id)
            if order_item is None: return         # Cancel
            if order_item == ":b":
                step -= 1
                continue
            step += 1

        if step == 4:
            if order_type == 'Delivery':
                threshold = db_fetch_delivery_threshold(store_id)
                # Wait to implement: check if total price meets threshold
                total_price = sum(item['subtotal'] for item in order_item)
                if total_price < threshold:
                    print(f"Delivery orders require a minimum total of ${threshold}. Your current total is ${total_price}.")
                    print("Do you want to change to Pickup instead (p), add more items and continue with Delivery (d), or go back to Store selection (b)?") 
                    step = 3
                    continue
                
            "Please confirm your order details here..."
            for o_item_id, details in order_item.items():
                print(f"{o_item_id}. Name: {details['product_name']}, Unit Price: {details['unit_price']}, "
                      f"Options: {details['customization']}, Option Price: {details['option_price']}, "
                      f"Quantity: {details['quantity']}, Subtotal: {details['subtotal']}")
            print("Total price:", sum(details['subtotal'] for details in order_item.values()))
            print("Leave blank and press Enter to confirm, or type the number to delete an item.")
            print("Type ':b' to go back to the previous step (Item selection). Your current items will be lost.")
            print("Type ':q' to cancel the order placement.")

                

                
    


    
        
        
        