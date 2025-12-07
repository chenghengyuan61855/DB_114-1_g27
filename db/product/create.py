# db/product/create.py
# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.crud import insert

def db_create_product_category(brand_id, p_category_name, p_category_description=None, display_order=None):
    """建立商品分類
    
    Args:
        brand_id: 品牌 ID
        p_category_name: 分類名稱
        p_category_description: 分類描述（可選）
        display_order: 顯示順序（可選）
    
    Returns:
        p_category_id: 新建立的分類 ID
    """
    row = insert("PRODUCT_CATEGORY", {
        "brand_id": brand_id,
        "p_category_name": p_category_name,
        "p_category_description": p_category_description,
        "display_order": display_order,
        "is_active": True,
    })
    return row[0]


def db_create_product(brand_id, product_name, p_category_id=None, size=None, 
                     product_description=None, image_url=None):
    """建立商品
    
    Args:
        brand_id: 品牌 ID
        product_name: 商品名稱
        p_category_id: 分類 ID（可選）
        size: 商品尺寸（如 S/M/L）
        product_description: 商品描述
        image_url: 圖片 URL
    
    Returns:
        product_id: 新建立的商品 ID
    """
    row = insert("PRODUCT", {
        "brand_id": brand_id,
        "product_name": product_name,
        "p_category_id": p_category_id,
        "size": size,
        "product_description": product_description,
        "image_url": image_url,
        "is_active": True,
    })
    return row[0]


def db_create_store_product(store_id, product_id, price):
    """建立門市販售商品（關聯門市與商品的價格）
    
    Args:
        store_id: 門市 ID
        product_id: 商品 ID
        price: 販售價格
    
    Returns:
        row: 完整的 STORE_PRODUCT 記錄
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    
    row = insert("STORE_PRODUCT", {
        "store_id": store_id,
        "product_id": product_id,
        "price": price,
        "is_active": True,
    })
    return row