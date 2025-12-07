# ui/product/create.py
# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.product.create import db_create_product_category, db_create_product, db_create_store_product
from ui.helper import cancel_check
from ui.product.helper import validate_product_name, validate_price

# def ui_create_product_category(brand_id):
#     """UI：建立商品分類"""
#     print("\n=== Create Product Category ===")
#     print("(Type ':q' to cancel)\n")
    
#     while True:
#         p_category_name = input("Category Name: ").strip()
#         if cancel_check(p_category_name, "Category Creation"):
#             return
        
#         if validate_product_name(p_category_name):
#             break
    
#     p_category_description = input("Description (optional): ").strip() or None
    
#     try:
#         display_order = input("Display Order (optional, default 0): ").strip()
#         if display_order:
#             display_order = int(display_order)
#         else:
#             display_order = None
#     except ValueError:
#         print("❌ Display order must be a number")
#         return
    
#     try:
#         p_category_id = db_create_product_category(
#             brand_id,
#             p_category_name,
#             p_category_description,
#             display_order
#         )
#         print(f"✅ Category created with ID: {p_category_id}")
#         return p_category_id
#     except Exception as e:
#         print(f"❌ Error: {e}")


def ui_create_product(brand_id):
    """UI：建立商品"""
    print("\n=== Create Product ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        product_name = input("Product Name: ").strip()
        if cancel_check(product_name, "Product Creation"):
            return
        
        if validate_product_name(product_name):
            break
    
    size = input("Size (optional, e.g., S/M/L): ").strip() or None
    product_description = input("Description (optional): ").strip() or None
    image_url = input("Image URL (optional): ").strip() or None
    
    # p_category_id = input("Category ID (optional): ").strip() or None
    # if p_category_id:
    #     try:
    #         p_category_id = int(p_category_id)
    #     except ValueError:
    #         print("❌ Category ID must be a number")
    #         return
    
    try:
        product_id = db_create_product(
            brand_id,
            product_name,
            p_category_id,
            size,
            product_description,
            image_url
        )
        print(f"✅ Product created with ID: {product_id}")
        return product_id
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_create_store_product(store_id):
    """UI：在門市新增販售商品"""
    print("\n=== Add Product to Store ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        product_id_str = input("Product ID: ").strip()
        if cancel_check(product_id_str, "Store Product Creation"):
            return
        
        try:
            product_id = int(product_id_str)
            break
        except ValueError:
            print("❌ Product ID must be a number")
    
    while True:
        price_str = input("Price: ").strip()
        if cancel_check(price_str, "Store Product Creation"):
            return
        
        if validate_price(price_str):
            price = int(price_str)
            break
    
    try:
        row = db_create_store_product(store_id, product_id, price)
        print(f"✅ Product added to store with price: {price}")
        return row
    except Exception as e:
        print(f"❌ Error: {e}")