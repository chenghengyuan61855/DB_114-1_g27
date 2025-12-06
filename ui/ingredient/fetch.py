# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.ingredient.fetch import db_fetch_ingredient, db_fetch_product_ingredient

def ui_view_ingredients(brand_id=None):
    """UI：查看原料列表"""
    try:
        ingredients = db_fetch_ingredient(brand_id=brand_id)
        if not ingredients:
            print("No ingredients found.")
            return
        
        print("\n=== Ingredient List ===")
        for ing in ingredients:
            print(f"ID: {ing['ingredient_id']} | Name: {ing['ingredient_name']} ({ing['unit']})")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_product_ingredients(product_id):
    """UI：查看商品使用的原料"""
    try:
        ingredients = db_fetch_product_ingredient(product_id)
        if not ingredients:
            print(f"No ingredients assigned to product {product_id}.")
            return
        
        print(f"\n=== Product {product_id} - Ingredients ===")
        for ing in ingredients:
            print(f"Ingredient ID: {ing['ingredient_id']} | Quantity: {ing['qty']}")
    except Exception as e:
        print(f"❌ Error: {e}")