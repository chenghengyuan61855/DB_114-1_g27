# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.option.fetch import (
    db_fetch_option_category,
    db_fetch_option,
    db_fetch_brand_product_option_rule,
    db_fetch_brand_product_option_mutex,
    db_fetch_store_option
)

def ui_view_option_categories(brand_id=None):
    """UI：查看選項分類列表"""
    try:
        categories = db_fetch_option_category(brand_id=brand_id)
        if not categories:
            print("No option categories found.")
            return
        
        print("\n=== Option Categories ===")
        for cat in categories:
            print(f"ID: {cat['o_category_id']} | Name: {cat['o_category_name']}")
            print(f"  Order: {cat['display_order']} | Active: {cat['is_active']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_options(o_category_id=None):
    """UI：查看選項列表"""
    try:
        options = db_fetch_option(o_category_id=o_category_id)
        if not options:
            print("No options found.")
            return
        
        print("\n=== Options ===")
        for opt in options:
            print(f"ID: {opt['option_id']} | Name: {opt['option_name']}")
            print(f"  Price Adjust: +{opt['price_adjust']}")
            if opt['ingredient_id']:
                print(f"  Ingredient: {opt['ingredient_id']}, Usage: {opt['usage_qty']}")
            print(f"  Active: {opt['is_active']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_product_option_rules(product_id):
    """UI：查看商品的選項規則"""
    try:
        rules = db_fetch_brand_product_option_rule(product_id=product_id)
        if not rules:
            print(f"No option rules found for product {product_id}.")
            return
        
        print(f"\n=== Product {product_id} - Option Rules ===")
        for rule in rules:
            print(f"Category: {rule['o_category_id']} | Min: {rule['min_select']}, Max: {rule['max_select']}")
            if rule['default_option_id']:
                print(f"  Default Option: {rule['default_option_id']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_product_option_mutex(product_id):
    """UI：查看商品的互斥選項規則"""
    try:
        mutex_rules = db_fetch_brand_product_option_mutex(product_id=product_id)
        if not mutex_rules:
            print(f"No mutex rules found for product {product_id}.")
            return
        
        print(f"\n=== Product {product_id} - Mutex Rules ===")
        for rule in mutex_rules:
            print(f"Option {rule['option_id_low']} <--> Option {rule['option_id_high']}")
            print(f"  Logic: {rule['mutex_logic']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_store_options(store_id):
    """UI：查看門市選項設定"""
    try:
        store_options = db_fetch_store_option(store_id=store_id)
        if not store_options:
            print(f"No options configured for store {store_id}.")
            return
        
        print(f"\n=== Store {store_id} - Options ===")
        for so in store_options:
            status = "✅ Enabled" if so['is_enabled'] else "❌ Disabled"
            print(f"Option {so['option_id']}: {status}")
    except Exception as e:
        print(f"❌ Error: {e}")