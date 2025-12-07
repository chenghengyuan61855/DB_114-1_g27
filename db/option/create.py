# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.crud import insert

def db_create_option_category(brand_id, o_category_name, display_order=None):
    """建立選項分類（如：甜度、冰度、配料）
    
    Args:
        brand_id: 品牌 ID
        o_category_name: 選項分類名稱
        display_order: 顯示順序（可選，用於 UI 排序）
    
    Returns:
        o_category_id: 新建立的選項分類 ID
    
    Raises:
        ValueError: 分類名稱無效
    """
    if not o_category_name or len(o_category_name) > 50:
        raise ValueError("Category name must be 1-50 characters")
    
    row = insert("OPTION_CATEGORY", {
        "brand_id": brand_id,
        "o_category_name": o_category_name,
        "display_order": display_order,
        "is_active": True,
    })
    return row[0]  # o_category_id


def db_create_option(o_category_id, option_name, price_adjust, ingredient_id=None, usage_qty=None):
    """建立選項（如：無糖、半糖、全糖）
    
    Args:
        o_category_id: 選項分類 ID
        option_name: 選項名稱
        price_adjust: 價格調整（可為負值表示優惠）
        ingredient_id: 原料 ID（可選，如果選項需要使用特定原料）
        usage_qty: 原料使用量（可選）
    
    Returns:
        option_id: 新建立的選項 ID
    
    Raises:
        ValueError: 參數無效
    """
    if not option_name or len(option_name) > 50:
        raise ValueError("Option name must be 1-50 characters")
    
    if price_adjust is None:
        price_adjust = 0
    
    if price_adjust < -1000 or price_adjust > 1000:
        raise ValueError("Price adjustment must be between -1000 and 1000")
    
    if (ingredient_id is not None and usage_qty is None) or (ingredient_id is None and usage_qty is not None):
        raise ValueError("Both ingredient_id and usage_qty must be provided together or both None")
    
    if usage_qty is not None and usage_qty < 0:
        raise ValueError("Usage quantity cannot be negative")
    
    row = insert("OPTION", {
        "o_category_id": o_category_id,
        "option_name": option_name,
        "price_adjust": price_adjust,
        "ingredient_id": ingredient_id,
        "usage_qty": usage_qty,
        "is_active": True,
    })
    return row[0]  # option_id


def db_create_brand_product_option_rule(brand_id, product_id, o_category_id, min_select, max_select, default_option_id=None):
    """建立商品選項規則（定義用戶必須選擇幾個該分類的選項）
    
    例如：
    - 甜度必選 1 個（min_select=1, max_select=1）
    - 配料最多選 3 個（min_select=0, max_select=3）
    
    Args:
        brand_id: 品牌 ID
        product_id: 商品 ID
        o_category_id: 選項分類 ID
        min_select: 最少要選幾個（0 表示可選）
        max_select: 最多可選幾個
        default_option_id: 預設選項 ID（可選）
    
    Returns:
        row: 完整規則記錄
    
    Raises:
        ValueError: 選擇數量邏輯無效
    """
    if min_select < 0 or max_select < 0:
        raise ValueError("min_select and max_select cannot be negative")
    
    if min_select > max_select:
        raise ValueError("min_select cannot be greater than max_select")
    
    row = insert("BRAND_PRODUCT_OPTION_RULE", {
        "brand_id": brand_id,
        "product_id": product_id,
        "o_category_id": o_category_id,
        "min_select": min_select,
        "max_select": max_select,
        "default_option_id": default_option_id,
    })
    return row


def db_create_brand_product_option_mutex(brand_id, product_id, option_id_low, option_id_high, mutex_logic):
    """建立選項互斥規則（定義哪些選項不能一起選）
    
    例如：
    - 「冰」和「熱」不能同時選
    - 「無糖」和「全糖」不能同時選
    
    Args:
        brand_id: 品牌 ID
        product_id: 商品 ID
        option_id_low: 選項 ID 1（應為較小的 ID）
        option_id_high: 選項 ID 2（應為較大的 ID）
        mutex_logic: 互斥邏輯（如 'EXCLUDE' 表示這兩個選項互斥）
    
    Returns:
        row: 互斥規則記錄
    
    Raises:
        ValueError: 選項 ID 邏輯無效
    """
    if option_id_low >= option_id_high:
        raise ValueError("option_id_low must be less than option_id_high")
    
    if mutex_logic not in ['single', 'exclusive']:
        raise ValueError("mutex_logic must be 'single' or 'exclusive'")
    
    row = insert("BRAND_PRODUCT_OPTION_MUTEX", {
        "brand_id": brand_id,
        "product_id": product_id,
        "option_id_low": option_id_low,
        "option_id_high": option_id_high,
        "mutex_logic": mutex_logic,
    })
    return row


def db_create_store_option(store_id, option_id, is_enabled=True):
    """設定門市是否啟用某個選項
    
    例如：
    - 某家分店沒有「珍珠」配料，可將其停用
    
    Args:
        store_id: 門市 ID
        option_id: 選項 ID
        is_enabled: 是否啟用（True=啟用，False=停用）
    
    Returns:
        row: 完整記錄
    """
    row = insert("STORE_OPTION", {
        "store_id": store_id,
        "option_id": option_id,
        "is_enabled": is_enabled,
    })
    return row