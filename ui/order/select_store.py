from db.crud import fetch
from ui.order.select_brand import ui_select_brand
from ui.helper import cancel_check
from ui.order.helper import go_back_check

def ui_show_order_accepting_stores(order_type, brand_id=None):
    conditions = {"is_accepting_orders": True}
    if order_type == "DELIVERY":
        conditions["is_accepting_deliveries"] = True
    if brand_id is not None:
        conditions["brand_id"] = brand_id

    stores = fetch("STORE", conditions, "store_id")

    if not stores:
        print("No stores are currently accepting orders with the specified criteria.")
        return []

    print("\nAvailable Stores:")
    for store in stores:
        print(f"{store[0]}. {store[2]} - {store[3]} (Phone: {store[4]})")

    return stores

def select_store_from_user(available_stores):
    while True:
        store_id = input("Enter Store ID to select a store: ").strip()
        if cancel_check(store_id, "Order Placement"):
            return None
        if go_back_check(store_id):
            return ":b"
        if store_id not in [str(store[0]) for store in available_stores]:
            print("Invalid Store ID. Please try again.")
            continue
        return int(store_id)

def ui_select_store(order_type, brand_id):
    """
    Prompts the user to select a store for the given brand and order type.
    If no stores are available for 'delivery', offers to switch to 'pickup'.
    Allows changing brand or cancelling when no stores are available.
    Returns the selected store_id or None if cancelled.
    """
    while True:
        available_stores = ui_show_order_accepting_stores(order_type, brand_id)
        if available_stores:
            return select_store_from_user(available_stores)

        if order_type == "delivery":
            pickup_stores = ui_show_order_accepting_stores("pickup", brand_id)
            if pickup_stores:
                while True:
                    decision = input(
                        "No stores currently offer delivery, but some offer pickup. Switch to pickup? (y/n): "
                    ).strip().lower()
                    if cancel_check(decision, "Order Placement"):
                        return None
                    if decision == "y":
                        order_type = "pickup"
                        return select_store_from_user(pickup_stores)
                    elif decision == "n":
                        break  # Proceed to brand selection below
                    else:
                        print("Invalid input. Please enter 'y', 'n', or ':q'.")

            else:
                print("No stores are currently accepting orders for the selected brand.")
        else:  # order_type == "pickup"
            print("No stores are currently accepting orders for the selected brand.")

        # Prompt for a new brand or cancel
        while True:
            decision = input("Select another brand (b) or quit (:q)? ").strip().lower()
            if cancel_check(decision, "Order Placement"):
                return None
            if decision == "b":
                brand_id = ui_select_brand()
                if not brand_id:
                    return None
                # Now restart the outer loop to try new brand
                break
            else:
                print("Invalid input. Please enter 'b' or ':q'.")