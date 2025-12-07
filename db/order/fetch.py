from db.crud import fetch, selective_fetch



def db_fetch_option_list(o_category_id):
    options = selective_fetch(
        "OPTION",
        ["option_id", "option_name", "price_adjust"],
        {"o_category_id": o_category_id, "is_active": True},
        "option_id")
    return options

def db_fetch_available_option_list(store_id, o_category_id):
    # Gets all enabled option ids for this store/o_category
    enabled = selective_fetch(
        "STORE_OPTION",
        ["option_id"],
        {"store_id": store_id, "o_category_id": o_category_id, "is_enabled": True},
        "option_id"
    )
    enabled_ids = {row[0] for row in enabled}
    # Filter overall options by available IDs
    all_opts = db_fetch_option_list(o_category_id)
    available = [opt for opt in all_opts if opt[0] in enabled_ids]
    return available

def db_fetch_option_rule(product_id, o_category_id):
    rules = selective_fetch(
        "BRAND_PRODUCT_OPTION_RULE",
        ["min_select", "max_select", "default_option_id"],
        {"product_id": product_id, "o_category_id": o_category_id}
    )
    if not rules:
        return {"min_select": 0, "max_select": 0, "default_option_id": None}
    rule = rules[0]
    return {
        "min_select": rule[0],
        "max_select": rule[1],
        "default_option_id": rule[2]
    }

def db_fetch_option_mutex(product_id, o_category_id):
    mutexes = selective_fetch(
        "BRAND_PRODUCT_OPTION_MUTEX",
        ["mutex_type", "option_id_low", "option_id_high"],
        {"product_id": product_id, "o_category_id": o_category_id}
    )
    return mutexes

def db_fetch_delivery_threshold(store_id):
    """
    Returns the minimum order total price (NTD integer) required for delivery at the given store.
    If not specified or the store does not exist, returns 0.
    """
    thresholds = selective_fetch("STORE", ["min_order_total_price"], {"store_id": store_id})
    if not thresholds or thresholds[0][0] is None:
        return 0
    try:
        return int(thresholds[0][0])
    except (TypeError, ValueError):
        return 0