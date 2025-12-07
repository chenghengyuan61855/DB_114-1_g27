from db.crud import fetch, selective_fetch


def db_fetch_option_list(o_category_id):
    """查詢某分類下的所有選項
    
    Args:
        o_category_id: 選項分類 ID
    
    Returns:
        list: [(option_id, option_name, price_adjust), ...]
    """
    options = selective_fetch(
        "OPTION",
        ["option_id", "option_name", "price_adjust"],
        {"o_category_id": o_category_id, "is_active": True},
        "option_id"
    )
    return options


def db_fetch_option_category_list(brand_id):
    """查詢品牌的所有選項分類
    
    Args:
        brand_id: 品牌 ID
    
    Returns:
        list: [(o_category_id, o_category_name), ...]
        
    Example:
        categories = db_fetch_option_category_list(1)
        # 返回：[(1, '甜度'), (2, '冰塊'), (3, '配料')]
    """
    categories = selective_fetch(
        "OPTION_CATEGORY",
        ["o_category_id", "o_category_name"],
        {"brand_id": brand_id, "is_active": True},
        "display_order"  # 按顯示順序排序
    )
    return categories


def db_fetch_available_option_list(store_id, o_category_id):
    """查詢門市在某分類下啟用的選項
    
    Args:
        store_id: 門市 ID
        o_category_id: 選項分類 ID
    
    Returns:
        list: [(option_id, option_name, price_adjust), ...]
    
    邏輯：
        1. 先取得該分類下的所有選項
        2. 查詢門市啟用的選項 ID
        3. 過濾出交集
    """
    # 1. 取得該分類的所有選項
    all_opts = db_fetch_option_list(o_category_id)
    
    if not all_opts:
        return []
    
    # 2. 查詢門市啟用的選項
    enabled = selective_fetch(
        "STORE_OPTION",
        ["option_id"],
        {"store_id": store_id, "is_enabled": True},
        "option_id"
    )
    
    # 3. 取得啟用的選項 ID 集合
    enabled_ids = {row[0] for row in enabled}
    
    # 4. 過濾出該分類中門市啟用的選項
    available = [opt for opt in all_opts if opt[0] in enabled_ids]
    
    return available


def db_fetch_option_rule(brand_id, product_id, o_category_id):
    """查詢商品選項規則
    
    Args:
        brand_id: 品牌 ID（新增）
        product_id: 商品 ID
        o_category_id: 選項分類 ID
    
    Returns:
        dict: {
            "min_select": int,
            "max_select": int,
            "default_option_id": int | None
        }
    """
    rules = selective_fetch(
        "BRAND_PRODUCT_OPTION_RULE",
        ["min_select", "max_select", "default_option_id"],
        {
            "brand_id": brand_id,          # ← 新增
            "product_id": product_id,
            "o_category_id": o_category_id
        }
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
    """查詢選項互斥規則
    
    Args:
        product_id: 商品 ID
        o_category_id: 選項分類 ID（暫未使用，保留供未來擴展）
    
    Returns:
        list: [(mutex_logic, option_id_low, option_id_high), ...]
    """
    mutexes = selective_fetch(
        "BRAND_PRODUCT_OPTION_MUTEX",
        ["mutex_logic", "option_id_low", "option_id_high"],
        {"product_id": product_id}
    )
    return mutexes


def db_fetch_delivery_threshold(store_id):
    """查詢門市的外送門檻
    
    Args:
        store_id: 門市 ID
    
    Returns:
        int: 外送最低金額（若無設定則返回 0）
    """
    stores = selective_fetch(
        "STORE",
        ["min_order_total_price"],
        {"store_id": store_id}
    )
    
    if not stores:
        return 0
    
    return stores[0][0] or 0