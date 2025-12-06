# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.ingredient.create import db_create_ingredient, db_create_product_ingredient
from ui.helper import cancel_check

def ui_create_ingredient(brand_id):
    """UI：建立原料"""
    print("\n=== Create Ingredient ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        ingredient_name = input("Ingredient Name (e.g., sugar, milk): ").strip()
        if cancel_check(ingredient_name, "Ingredient Creation"):
            return
        
        if len(ingredient_name) > 0 and len(ingredient_name) <= 100:
            break
        else:
            print("❌ Name must be 1-100 characters.")
    
    print("\nUnit options: 'g' (gram), 'ml' (milliliter), 'piece'")
    while True:
        unit = input("Unit: ").strip().lower()
        if cancel_check(unit, "Ingredient Creation"):
            return
        
        if unit in ['g', 'ml', 'piece']:
            break
        else:
            print("❌ Unit must be 'g', 'ml', or 'piece'")
    
    try:
        ingredient_id = db_create_ingredient(brand_id, ingredient_name, unit)
        print(f"✅ Ingredient created with ID: {ingredient_id}")
        return ingredient_id
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_add_ingredient_to_product(product_id):
    """UI：新增商品使用的原料"""
    print("\n=== Add Ingredient to Product ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        ingredient_id_str = input("Ingredient ID: ").strip()
        if cancel_check(ingredient_id_str, "Add Ingredient"):
            return
        
        try:
            ingredient_id = int(ingredient_id_str)
            break
        except ValueError:
            print("❌ Ingredient ID must be a number")
    
    while True:
        qty_str = input("Quantity: ").strip()
        if cancel_check(qty_str, "Add Ingredient"):
            return
        
        try:
            qty = int(qty_str)
            if qty < 0:
                print("❌ Quantity cannot be negative")
                continue
            break
        except ValueError:
            print("❌ Quantity must be a number")
    
    try:
        row = db_create_product_ingredient(product_id, ingredient_id, qty)
        print(f"✅ Ingredient added to product")
        return row
    except Exception as e:
        print(f"❌ Error: {e}")