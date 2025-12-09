from db.crud import selective_fetch

def db_fetch_is_accepting_orders(store_id):
    """查詢門市是否接受訂單
    
    Args:
        store_id: 門市 ID
    
    Returns:
        bool: 是否接受訂單
    """
    result = selective_fetch(
        "STORE",
        ["is_accepting_orders"],
        {"store_id": store_id}
    )
    if result:
        return result[0][0]
    else:
        return False  # 門市不存在時，預設不接受訂單
    
def db_fetch_is_accepting_deliveries(store_id):
    """查詢門市是否接受外送訂單
    
    Args:
        store_id: 門市 ID
    
    Returns:
        bool: 是否接受外送訂單
    """
    result = selective_fetch(
        "STORE",
        ["is_accepting_deliveries"],
        {"store_id": store_id}
    )
    if result:
        return result[0][0]
    else:
        return False  # 門市不存在時，預設不接受外送訂單