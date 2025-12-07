# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.crud import update, delete

def db_update_option_category(o_category_id, **updates):
    """更新選項分類
    
    Args:
        o_category_id: 選項分類 ID
        **updates: 要更新的欄位（如 o_category_name, display_order, is_active）
    
    Returns:
        int: 受影響的行數
    """
    if not updates:
        raise ValueError("No fields to update")
    
    row = update("OPTION_CATEGORY", updates, {"o_category_id": o_category_id})
    return row


def db_update_option(option_id, **updates):
    """更新選項
    
    Args:
        option_id: 選項 ID
        **updates: 要更新的欄位（如 option_name, price_adjust, is_active）
    
    Returns:
        int: 受影響的行數
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證 price_adjust
    if "price_adjust" in updates:
        if updates["price_adjust"] < -1000 or updates["price_adjust"] > 1000:
            raise ValueError("Price adjustment must be between -1000 and 1000")
    
    row = update("OPTION", updates, {"option_id": option_id})
    return row


def db_update_brand_product_option_rule(brand_id, product_id, o_category_id, **updates):
    """更新商品選項規則
    
    Args:
        brand_id: 品牌 ID
        product_id: 商品 ID
        o_category_id: 選項分類 ID
        **updates: 要更新的欄位（如 min_select, max_select, default_option_id）
    
    Returns:
        int: 受影響的行數
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證選擇範圍
    if "min_select" in updates or "max_select" in updates:
        min_select = updates.get("min_select", 0)
        max_select = updates.get("max_select", 0)
        
        if min_select < 0 or max_select < 0:
            raise ValueError("Min and max select cannot be negative")
        
        if min_select > max_select:
            raise ValueError("Min select cannot be greater than max select")
    
    conditions = {
        "brand_id": brand_id,
        "product_id": product_id,
        "o_category_id": o_category_id
    }
    
    row = update("BRAND_PRODUCT_OPTION_RULE", updates, conditions)
    return row


def db_update_store_option(store_id, option_id, is_enabled):
    """更新門市選項狀態
    
    Args:
        store_id: 門市 ID
        option_id: 選項 ID
        is_enabled: 是否啟用
    
    Returns:
        int: 受影響的行數
    """
    row = update("STORE_OPTION", {"is_enabled": is_enabled}, {"store_id": store_id, "option_id": option_id})
    return row


def db_delete_option_category(o_category_id):
    """刪除選項分類（軟刪除：設定 is_active = False）
    
    Args:
        o_category_id: 選項分類 ID
    
    Returns:
        int: 受影響的行數
    """
    row = update("OPTION_CATEGORY", {"is_active": False}, {"o_category_id": o_category_id})
    return row


def db_delete_option(option_id):
    """刪除選項（軟刪除：設定 is_active = False）
    
    Args:
        option_id: 選項 ID
    
    Returns:
        int: 受影響的行數
    """
    row = update("OPTION", {"is_active": False}, {"option_id": option_id})
    return row


def db_delete_brand_product_option_rule(brand_id, product_id, o_category_id):
    """刪除商品選項規則
    
    Args:
        brand_id: 品牌 ID
        product_id: 商品 ID
        o_category_id: 選項分類 ID
    
    Returns:
        int: 受影響的行數
    """
    conditions = {
        "brand_id": brand_id,
        "product_id": product_id,
        "o_category_id": o_category_id
    }
    
    row = delete("BRAND_PRODUCT_OPTION_RULE", conditions)
    return row


def db_delete_brand_product_option_mutex(mutex_id):
    """刪除互斥選項規則
    
    Args:
        mutex_id: 互斥規則 ID
    
    Returns:
        int: 受影響的行數
    """
    row = delete("BRAND_PRODUCT_OPTION_MUTEX", {"mutex_id": mutex_id})
    return row


def db_delete_store_option(store_id, option_id):
    """刪除門市選項設定
    
    Args:
        store_id: 門市 ID
        option_id: 選項 ID
    
    Returns:
        int: 受影響的行數
    """
    row = delete("STORE_OPTION", {"store_id": store_id, "option_id": option_id})
    return row