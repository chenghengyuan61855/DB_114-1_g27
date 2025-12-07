from db.crud import fetch

def ui_show_order_accepting_stores(order_type, brand_id=None):
    conditions = {"is_accepting_orders": True}
    if order_type == "DELIVERY":
        conditions["is_accepting_deliveries"] = True
    if brand_id is not None:
        conditions["brand_id"] = brand_id

    stores = fetch("STORE", conditions, "store_id")

    print("\nAvailable Stores:")
    for store in stores:
        print(f"{store[0]}. {store[2]} - {store[3]} (Phone: {store[4]})")

    return stores