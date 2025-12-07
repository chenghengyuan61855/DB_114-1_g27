from db.crud import fetch, fetch_in
from ui.helper import cancel_check, clear_screen  # ← 新增導入 clear_screen
from ui.order.helper import go_back_check

def ui_show_available_products(store_id):
    """顯示門市可購買的商品"""
    # 1. 查詢門市販售的商品
    products = fetch("STORE_PRODUCT", {"store_id": store_id, "is_active": True}, "product_id")

    if not products:
        print("No products available in the selected store.")
        return []
    
    # 2. 取得所有 product_id
    product_ids = [product[1] for product in products]
    
    # 3. 使用 fetch_in 一次查詢所有商品
    products_detail = fetch_in("PRODUCT", "product_id", product_ids, "product_id")
    
    if not products_detail:
        print("No product details found.")
        return []
    
    cleaned_products = []

    clear_screen()  # ← 新增：顯示商品列表前清屏
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
    """選擇商品並輸入數量"""
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
        
        for pid, pname, pprice in cleaned_products:
            if pid == int(product_id):
                product_name = pname
                unit_price = pprice
                break
        
        return int(product_id), product_name, int(unit_price), int(qty)