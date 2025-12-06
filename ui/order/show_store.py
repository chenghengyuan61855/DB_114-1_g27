from db.crud import fetch

def ui_show_order_accepting_stores(brand_id=None, criterias=None):
    conditions = {}
    if brand_id is not None:
        conditions["brand_id"] = brand_id

    stores = fetch("STORE", conditions)
    store_list = []
    for row in stores:
        store_info = {
            "store_id": row[0],
            "store_name": row[2],
            "address": row[3],
            "phone": row[4],
        }
        store_list.append(store_info)

    return store_list

def ui_show_delivery_accepting_stores(brand_id=None):
    criteria = {}
    if brand_id is not None:
        criteria["brand_id"] = brand_id

    stores = fetch("STORE", criteria)
    store_list = []
    for row in stores:
        if row[5] and row[6] and row[7]: #is_active at index 5, is_accepting_orders at index 6, is_accepting_delivery at index 7
            store_info = {
                "store_id": row[0],
                "store_name": row[2],
                "address": row[3],
                "phone": row[4],
            }
            store_list.append(store_info)

    return store_list

