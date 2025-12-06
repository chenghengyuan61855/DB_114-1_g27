# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.crud import fetch

def db_fetch_ingredient(ingredient_id=None, brand_id=None):
    """查詢原料
    
    Args:
        ingredient_id: 原料 ID（精確查詢）
        brand_id: 品牌 ID（查該品牌所有原料）
    
    Returns:
        list: 原料列表
    """
    conditions = {}
    if ingredient_id:
        conditions["ingredient_id"] = ingredient_id
    if brand_id:
        conditions["brand_id"] = brand_id
    
    rows = fetch("INGREDIENT", conditions if conditions else None)
    return [
        {
            "ingredient_id": row[0],
            "brand_id": row[1],
            "ingredient_name": row[2],
            "unit": row[3],
            "is_active": row[4],
        }
        for row in rows
    ]


def db_fetch_product_ingredient(product_id=None):
    """查詢商品使用的原料
    
    Args:
        product_id: 商品 ID
    
    Returns:
        list: 原料清單
    """
    conditions = {}
    if product_id:
        conditions["product_id"] = product_id
    
    rows = fetch("PRODUCT_INGREDIENT", conditions if conditions else None)
    return [
        {
            "product_id": row[0],
            "ingredient_id": row[1],
            "qty": row[2],
        }
        for row in rows
    ]