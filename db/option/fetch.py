# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.crud import fetch

def db_fetch_option_category(o_category_id=None, brand_id=None):
    """查詢選項分類
    
    Args:
        o_category_id: 選項分類 ID（精確查詢）
        brand_id: 品牌 ID（查該品牌所有分類）
    
    Returns:
        list: 選項分類列表
    """
    conditions = {}
    if o_category_id:
        conditions["o_category_id"] = o_category_id
    if brand_id:
        conditions["brand_id"] = brand_id
    
    rows = fetch("OPTION_CATEGORY", conditions if conditions else None)
    return [
        {
            "o_category_id": row[0],
            "brand_id": row[1],
            "o_category_name": row[2],
            "display_order": row[3],
            "is_active": row[4],
        }
        for row in rows
    ]


def db_fetch_option(option_id=None, o_category_id=None):
    """查詢選項
    
    Args:
        option_id: 選項 ID（精確查詢）
        o_category_id: 選項分類 ID（查該分類下所有選項）
    
    Returns:
        list: 選項列表
    """
    conditions = {}
    if option_id:
        conditions["option_id"] = option_id
    if o_category_id:
        conditions["o_category_id"] = o_category_id
    
    rows = fetch("OPTION", conditions if conditions else None)
    return [
        {
            "option_id": row[0],
            "o_category_id": row[1],
            "option_name": row[2],
            "price_adjust": row[3],
            "ingredient_id": row[4],
            "usage_qty": row[5],
            "is_active": row[6],
        }
        for row in rows
    ]


def db_fetch_brand_product_option_rule(brand_id=None, product_id=None, o_category_id=None):
    """查詢商品選項規則
    
    Args:
        brand_id: 品牌 ID
        product_id: 商品 ID
        o_category_id: 選項分類 ID
    
    Returns:
        list: 規則列表
    """
    conditions = {}
    if brand_id:
        conditions["brand_id"] = brand_id
    if product_id:
        conditions["product_id"] = product_id
    if o_category_id:
        conditions["o_category_id"] = o_category_id
    
    rows = fetch("BRAND_PRODUCT_OPTION_RULE", conditions if conditions else None)
    return [
        {
            "brand_id": row[0],
            "product_id": row[1],
            "o_category_id": row[2],
            "min_select": row[3],
            "max_select": row[4],
            "default_option_id": row[5],
        }
        for row in rows
    ]


def db_fetch_brand_product_option_mutex(brand_id=None, product_id=None):
    """查詢商品的互斥選項規則
    
    Args:
        brand_id: 品牌 ID
        product_id: 商品 ID
    
    Returns:
        list: 互斥規則列表
    """
    conditions = {}
    if brand_id:
        conditions["brand_id"] = brand_id
    if product_id:
        conditions["product_id"] = product_id
    
    rows = fetch("BRAND_PRODUCT_OPTION_MUTEX", conditions if conditions else None)
    return [
        {
            "mutex_id": row[0],
            "brand_id": row[1],
            "product_id": row[2],
            "option_id_low": row[3],
            "option_id_high": row[4],
            "mutex_logic": row[5],
        }
        for row in rows
    ]


def db_fetch_store_option(store_id=None, option_id=None):
    """查詢門市選項設定
    
    Args:
        store_id: 門市 ID
        option_id: 選項 ID
    
    Returns:
        list: 門市選項列表
    """
    conditions = {}
    if store_id:
        conditions["store_id"] = store_id
    if option_id:
        conditions["option_id"] = option_id
    
    rows = fetch("STORE_OPTION", conditions if conditions else None)
    return [
        {
            "store_id": row[0],
            "option_id": row[1],
            "is_enabled": row[2],
        }
        for row in rows
    ]