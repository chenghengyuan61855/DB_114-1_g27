from db.crud import selective_fetch
from ui.helper import cancel_check
from ui.order.helper import go_back_check
from db.order.fetch import db_fetch_available_option_list, db_fetch_option_rule, db_fetch_option_mutex

def ui_select_options_in_category(store_id, product_id, o_category_id):
    """
    UI for selecting options in a category, with enforcement of business rules.
    Returns a list of option_ids selected (or default if allowed and no selection).
    """

    # 1. Prepare data
    enabled_options = db_fetch_available_option_list(store_id, o_category_id)   # [ (option_id, option_name, price_adjust), ... ]
    rule = db_fetch_option_rule(product_id, o_category_id)            # min_select, max_select, default_option_id
    mutexes = db_fetch_option_mutex(product_id, o_category_id)        # [("single", id1, None), ("exclusive", id2, id3), ...]
    unavailable_ids = [mutex[1] for mutex in mutexes if mutex[0] == 'single']
    valid_options = [opt for opt in enabled_options if opt[0] not in unavailable_ids]
    unavailable_options = [opt for opt in enabled_options if opt[0] in unavailable_ids]

    valid_ids = [opt[0] for opt in valid_options]
    default_id = rule.get('default_option_id')
    min_select = rule.get('min_select', 0)
    max_select = rule.get('max_select', len(valid_options))

    mutex_dict = {}
    for mutype, oid1, oid2 in mutexes:
        if mutype == 'exclusive':
            mutex_dict.setdefault(oid1, set()).add(oid2)
            mutex_dict.setdefault(oid2, set()).add(oid1)

    if min_select == 0 and max_select == 0:
        if default_id is not None:
            print(f"No selection needed. Default option {default_id} will be applied.")
            return [int(default_id)]
        else:
            print("No options need to be selected in this category.")
            return []

    print(f"Please select {min_select} to {max_select} option(s):")
    for opt in valid_options:
        print(f"- {opt[0]}: {opt[1]} (+${opt[2]})")
    for opt in unavailable_options:
        print(f"- {opt[0]}: {opt[1]} (Not available)")

    print("Enter option IDs separated by spaces. Use ':q' to cancel, ':b' to go back.")

    # 3. Selection loop
    while True:
        input_options = input("Choose option(s): ").strip()
        if cancel_check(input_options, "Option Selection"):
            return None
        if go_back_check(input_options):
            return ":b"
        ids = input_options.split()

        # Validate IDs
        if not all(i in map(str, valid_ids) for i in ids):
            print("Invalid option ID(s). Try again.")
            continue
        ids = set(map(int, ids))

        # Apply mutex rules
        for sid in ids:
            if sid in mutex_dict and not mutex_dict[sid].isdisjoint(ids - {sid}):
                conflicting = sorted(list(mutex_dict[sid].intersection(ids)))
                print(f"Option {sid} cannot be selected together with {conflicting}. Try again.")
                break
        else:
            if not (min_select <= len(ids) <= max_select):
                print(f"Please select between {min_select} and {max_select} options.")
                continue

            subtotal = sum(int(opt[2]) for opt in valid_options if opt[0] in ids)
            return list(ids), subtotal


def ui_select_options(brand_id, store_id, product_id):
    option_categories = selective_fetch(
        "OPTION_CATEGORY",
        ["o_category_id", "o_category_name"],
        {"brand_id": brand_id, "is_active": True}, "display_order")

    if not option_categories:
        print("No options available for the selected product.")
        return None
    
    selected_options = {}
    category_option_price = {}
    substep = 0
    total_option_price = 0

    while True:
        if substep >= len(option_categories):
            break

        o_category = option_categories[substep]
        o_category_id = o_category[0]
        o_category_name = o_category[1]

        print(f"\n--- Option Category: {o_category_name} ---")
        result = ui_select_options_in_category(store_id, product_id, o_category_id)
        if result is None:
            return None
        if result == ":b":
            if substep > 0:
                last_category_id = option_categories[substep - 1][0]
                total_option_price -= category_option_price.get(last_category_id, 0)
                selected_options.pop(last_category_id, None)
                category_option_price.pop(last_category_id, None)
                substep -= 1
            else:
                print("Already at the first option category.")
            continue

        option_ids, option_price = result
        selected_options[o_category_id] = option_ids
        category_option_price[o_category_id] = option_price
        total_option_price += option_price
        substep += 1

    
    return selected_options, total_option_price
