from db.crud import fetch
from ui.helper import cancel_check
from ui.order.helper import go_back_check

def ui_show_available_products(store_id):
    products = fetch("STORE_PRODUCT", {"store_id": store_id, "is_active": True}, "product_id")
    products_detail = fetch("PRODUCT", {"product_id": [product[1] for product in products]}, "product_id")

    if not products:
        print("No products available in the selected store.")
        return []
    
    cleaned_products = []

    print("\nAvailable Products:")
    for i, product in enumerate(products):
        product_id = product[1]
        product_name = products_detail[i][2]
        size = products_detail[i][3]
        pro = f"{product_name} ({size})" if size else product_name
        price = product[2]
        description = products_detail[i][4]
        cleaned_products.append((product_id, pro, price))
        print(f"{product_id}. {pro} - ${price}")
        print(f"   Description: {description}")

    return cleaned_products

def ui_select_product(store_id):
    cleaned_products = ui_show_available_products(store_id)

    if not cleaned_products:
        print("No products available in the selected store.")
        return None
    
    while True:
        product_id = input("Enter Product ID to select a product: ").strip()
        if cancel_check(product_id, "Order placement"):
            return None
        if go_back_check(product_id):
            return ":b"
        if product_id not in [str(pid) for pid, _, _ in cleaned_products]:
            print("Invalid Product ID. Please try again.")
            continue
        qty = input("Enter quantity: ").strip()
        if cancel_check(qty, "Order placement"):
            return None
        if go_back_check(qty):
            return ":b"
        if not qty.isdigit() or int(qty) <= 0:
            print("Invalid quantity. Please enter a positive integer.")
            continue
        product_name = cleaned_products[int(product_id)-1][1]
        unit_price = cleaned_products[int(product_id)-1][2]
        return int(product_id), product_name, int(unit_price), int(qty)