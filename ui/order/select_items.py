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
        
        # option_data = (all_options, total_option_price)
        # all_options = {category_name: [option_ids]}
        all_options_dict, option_price = option_data
        
        # 將所有選項 ID 展平成一個列表
        selected_option_ids = []
        customization_text = []
        for category_name, option_ids in all_options_dict.items():
            selected_option_ids.extend(option_ids)
            customization_text.append(f"{category_name}: {option_ids}")
        
        customization_str = ", ".join(customization_text) if customization_text else "No customization"
        
        selected_items.append({
            "product_id": product_id,
            "product_name": product_name,
            "unit_price": unit_price,
            "customization": customization_str,
            "option_price": option_price,
            "quantity": qty,
            "subtotal": (unit_price + option_price) * qty,
            "selected_options": selected_option_ids  # ✅ 新增：儲存選項 ID 列表
        })
        print(f"Added {qty} x {product_name} to order.")
        more = input("Do you want to add more items? (y/n): ").strip().lower()
        if more == 'n':
            return selected_items
