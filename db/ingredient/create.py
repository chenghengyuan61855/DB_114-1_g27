# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-06
# ASSISTED BY: Claude
# ============================

from db.crud import insert

def db_create_ingredient(brand_id, ingredient_name, unit):
    """建立原料
    
    Args:
        brand_id: 品牌 ID
        ingredient_name: 原料名稱（如：砂糖、牛奶）
        unit: 單位（'g' / 'ml' / 'piece'）
    
    Returns:
        ingredient_id: 新建立的原料 ID
    
    Raises:
        ValueError: 單位無效
    """
    if unit not in ['g', 'ml', 'piece']:
        raise ValueError(f"Invalid unit: {unit}. Must be 'g', 'ml', or 'piece'")
    
    row = insert("INGREDIENT", {
        "brand_id": brand_id,
        "ingredient_name": ingredient_name,
        "unit": unit,
        "is_active": True,
    })
    return row[0]  # ingredient_id


def db_create_product_ingredient(product_id, ingredient_id, qty):
    """建立商品使用的原料關係
    
    Args:
        product_id: 商品 ID
        ingredient_id: 原料 ID
        qty: 使用量（單位根據原料定義）
    
    Returns:
        row: 完整記錄
    
    Raises:
        ValueError: 用量無效
    """
    if qty < 0:
        raise ValueError("Quantity cannot be negative")
    
    row = insert("PRODUCT_INGREDIENT", {
        "product_id": product_id,
        "ingredient_id": ingredient_id,
        "qty": qty,
    })
    return row