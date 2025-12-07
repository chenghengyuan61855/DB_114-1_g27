from db.crud import fetch
from ui.helper import cancel_check
from ui.order.helper import go_back_check

def ui_select_option(brand_id, product_id):
    option_categories = fetch("O"

    if not options:
        print("No options available for the selected product.")
        return None

    option_ids = []

    print("\nAvailable Options:")
    for option in options:
        option_id = option[2]
        option_name = option[3]
        additional_price = option[4]
        option_ids.append(option_id)
        price_info = f" (+${additional_price})" if additional_price > 0 else ""
        print(f"{option_id}. {option_name}{price_info}")

    while True:
        option_id = input("Enter Option ID to select an option: ").strip()
        if cancel_check(option_id, "Order placement"):
            return None
        if go_back_check(option_id):
            return ":b"
        if option_id not in [str(oid) for oid in option_ids]:
            print("Invalid Option ID. Please try again.")
            continue
        return int(option_id)