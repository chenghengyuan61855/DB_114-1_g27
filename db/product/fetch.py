# db/product/fetch.py
# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.crud import fetch

# def db_fetch_product_categories(brand_id=None):
#     """查詢商品分類
    
#     Args:
#         brand_id: 品牌 ID（如果指定則只查該品牌的分類）
    
#     Returns:
#         list: 分類列表
#     """
#     conditions = {}
#     if brand_id:
#         conditions["brand_id"] = brand_id
    
#     rows = fetch("PRODUCT_CATEGORY", conditions if conditions else None)
#     return [
#         {
#             "p_category_id": row[0],
#             "brand_id": row[1],
#             "p_category_name": row[2],
#             "p_category_description": row[3],
#             "display_order": row[4],
#             "is_active": row[5],
#         }
#         for row in rows
#     ]


def db_fetch_product(product_id=None, brand_id=None):
    """查詢商品
    
    Args:
        product_id: 商品 ID（精確查詢）
        brand_id: 品牌 ID（查該品牌所有商品）
    
    Returns:
        list: 商品列表
    """
    conditions = {}
    if product_id:
        conditions["product_id"] = product_id
    if brand_id:
        conditions["brand_id"] = brand_id
    
    rows = fetch("PRODUCT", conditions if conditions else None)
    return [
        {
            "product_id": row[0],
            "brand_id": row[1],
            "product_name": row[2],      # ← 調整索引（原本是 row[3]）
            "size": row[3],               # ← 調整索引（原本是 row[4]）
            "product_description": row[4], # ← 調整索引（原本是 row[5]）
            "image_url": row[5],          # ← 調整索引（原本是 row[6]）
            "is_active": row[6],          # ← 調整索引（原本是 row[7]）
        }
        for row in rows
    ]


def db_fetch_store_product(store_id=None, product_id=None):
    """查詢門市販售的商品
    
    Args:
        store_id: 門市 ID
        product_id: 商品 ID
    
    Returns:
        list: 門市商品列表
    """
    conditions = {}
    if store_id:
        conditions["store_id"] = store_id
    if product_id:
        conditions["product_id"] = product_id
    
    rows = fetch("STORE_PRODUCT", conditions if conditions else None)
    return [
        {
            "store_id": row[0],
            "product_id": row[1],
            "price": row[2],
            "is_active": row[3],
        }
        for row in rows
    ]