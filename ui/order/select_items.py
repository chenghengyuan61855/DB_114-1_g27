from ui.order.select_product import ui_select_product
from ui.order.select_options import ui_select_options


def ui_select_items(brand_id, store_id):
    print("\n--- Select Items ---")
    print("Selected options are currently uneditable. If you want to change options, please reselect the product.")
    print("You may delete the previous item after all selections are made.")
    print("Type ':b' in any input to go back to the previous step (Store selection) Current items would be lost.")
    print("Type ':q' in any input to cancel your order.")

    selected_items = []
    while True:
        item_data = ui_select_product(store_id)
        if item_data is None: return None     # Cancel
        if item_data == ":b":
                return ":b"
        product_id, product_name, unit_price, qty = item_data
        
        option_data = ui_select_options(brand_id, store_id, product_id)
        if option_data is None: return None      # Cancel
        selected_items.append({
            "product_id": product_id,
            "product_name": product_name,
            "unit_price": unit_price,
            "customization": option_data[0],
            "option_price": option_data[1],
            "quantity": qty,
            "subtotal": (unit_price + option_data[1]) * qty
        })
        print(f"Added {qty} x {product_name} to order.")
        more = input("Do you want to add more items? (y/n): ").strip().lower()
        if more == 'n':
            return selected_items
