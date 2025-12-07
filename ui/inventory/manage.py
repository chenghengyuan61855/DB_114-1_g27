# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.inventory.manage import (
    db_create_inventory, 
    db_fetch_inventory, 
    db_update_inventory,
    db_deduct_inventory
)
from ui.helper import cancel_check

def ui_create_inventory(store_id):
    """UI：建立庫存記錄"""
    print("\n=== Create Inventory ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        ingredient_id_str = input("Ingredient ID: ").strip()
        if cancel_check(ingredient_id_str, "Inventory Creation"):
            return
        
        try:
            ingredient_id = int(ingredient_id_str)
            break
        except ValueError:
            print("❌ Ingredient ID must be a number")
    
    while True:
        stock_str = input("Stock Level: ").strip()
        if cancel_check(stock_str, "Inventory Creation"):
            return
        
        try:
            stock_level = int(stock_str)
            if stock_level < 0:
                print("❌ Stock level cannot be negative")
                continue
            break
        except ValueError:
            print("❌ Stock level must be a number")
    
    try:
        row = db_create_inventory(store_id, ingredient_id, stock_level)
        print(f"✅ Inventory created successfully")
        return row
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_inventory(store_id):
    """UI：查看門市庫存"""
    try:
        inventory = db_fetch_inventory(store_id=store_id)
        if not inventory:
            print(f"No inventory found for store {store_id}.")
            return
        
        print(f"\n=== Store {store_id} - Inventory ===")
        for inv in inventory:
            print(f"Ingredient ID: {inv['ingredient_id']} | Stock: {inv['stock_level']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_update_inventory(store_id):
    """UI：更新庫存"""
    print("\n=== Update Inventory ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        ingredient_id_str = input("Ingredient ID: ").strip()
        if cancel_check(ingredient_id_str, "Update Inventory"):
            return
        
        try:
            ingredient_id = int(ingredient_id_str)
            break
        except ValueError:
            print("❌ Ingredient ID must be a number")
    
    while True:
        new_stock_str = input("New Stock Level: ").strip()
        if cancel_check(new_stock_str, "Update Inventory"):
            return
        
        try:
            new_stock_level = int(new_stock_str)
            if new_stock_level < 0:
                print("❌ Stock level cannot be negative")
                continue
            break
        except ValueError:
            print("❌ Stock level must be a number")
    
    try:
        db_update_inventory(store_id, ingredient_id, new_stock_level)
        print(f"✅ Inventory updated successfully")
    except Exception as e:
        print(f"❌ Error: {e}")