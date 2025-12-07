# ui/product/fetch.py
# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.product.fetch import db_fetch_product, db_fetch_store_product

def ui_view_products(brand_id=None):
    """UI：查看商品列表"""
    try:
        products = db_fetch_product(brand_id=brand_id)
        if not products:
            print("No products found.")
            return
        
        print("\n=== Product List ===")
        for p in products:
            print(f"\nID: {p['product_id']} | Name: {p['product_name']}")
            print(f"  Size: {p['size'] or 'N/A'}")
            # print(f"  Category: {p['p_category_id'] or 'N/A'}")
            print(f"  Description: {p['product_description'] or 'N/A'}")
            print(f"  Active: {p['is_active']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_store_products(store_id):
    """UI：查看門市販售的商品"""
    try:
        store_products = db_fetch_store_product(store_id=store_id)
        if not store_products:
            print("No products found for this store.")
            return
        
        print(f"\n=== Store {store_id} - Products ===")
        for sp in store_products:
            print(f"Product ID: {sp['product_id']} | Price: ${sp['price']}")
    except Exception as e:
        print(f"❌ Error: {e}")