# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.option.create import (
    db_create_option_category,
    db_create_option,
    db_create_brand_product_option_rule,
    db_create_brand_product_option_mutex,
    db_create_store_option
)
from ui.helper import cancel_check
from ui.option.helper import (
    validate_category_name,
    validate_option_name,
    validate_price_adjust,
    validate_select_range
)

def ui_create_option_category(brand_id):
    """UI：建立選項分類"""
    print("\n=== Create Option Category ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        category_name = input("Category Name (e.g., Sweetness, Ice Level): ").strip()
        if cancel_check(category_name, "Category Creation"):
            return
        
        if validate_category_name(category_name):
            break
    
    display_order = input("Display Order (optional, default 0): ").strip() or "0"
    try:
        display_order = int(display_order)
    except ValueError:
        print("❌ Display order must be a number")
        return
    
    try:
        o_category_id = db_create_option_category(brand_id, category_name, display_order)
        print(f"✅ Category created with ID: {o_category_id}")
        return o_category_id
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_create_option(o_category_id):
    """UI：建立選項"""
    print("\n=== Create Option ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        option_name = input("Option Name: ").strip()
        if cancel_check(option_name, "Option Creation"):
            return
        
        if validate_option_name(option_name):
            break
    
    while True:
        price_str = input("Price Adjustment (-1000 to 1000): ").strip()
        if cancel_check(price_str, "Option Creation"):
            return
        
        if validate_price_adjust(price_str):
            price_adjust = int(price_str)
            break
    
    # ⚠️ 暫時移除 ingredient_id 輸入
    # ingredient_id_str = input("Ingredient ID (optional): ").strip() or None
    # if ingredient_id_str:
    #     try:
    #         ingredient_id = int(ingredient_id_str)
    #     except ValueError:
    #         print("❌ Ingredient ID must be a number")
    #         return
    
    try:
        option_id = db_create_option(
            o_category_id,
            option_name,
            price_adjust
            # ⚠️ 暫時移除 ingredient_id
        )
        print(f"✅ Option created with ID: {option_id}")
        return option_id
    except Exception as e:
        print(f"❌ Error: {e}")


# def ui_create_option(o_category_id):
#     """UI：建立選項"""
#     print("\n=== Create Option ===")
#     print("(Type ':q' to cancel)\n")
    
#     while True:
#         option_name = input("Option Name (e.g., No Sugar, Half Sugar): ").strip()
#         if cancel_check(option_name, "Option Creation"):
#             return
        
#         if validate_option_name(option_name):
#             break
    
#     while True:
#         price_adjust_str = input("Price Adjustment (default 0): ").strip() or "0"
#         if cancel_check(price_adjust_str, "Option Creation"):
#             return
        
#         if validate_price_adjust(price_adjust_str):
#             price_adjust = int(price_adjust_str)
#             break
    
#     # 詢問是否需要添加原料
#     add_ingredient = input("Add ingredient to this option? (y/n, default n): ").strip().lower()
#     ingredient_id = None
#     usage_qty = None
    
#     if add_ingredient == 'y':
#         while True:
#             ingredient_id_str = input("Ingredient ID: ").strip()
#             if cancel_check(ingredient_id_str, "Option Creation"):
#                 return
            
#             try:
#                 ingredient_id = int(ingredient_id_str)
#                 break
#             except ValueError:
#                 print("❌ Ingredient ID must be a number")
        
#         while True:
#             usage_qty_str = input("Usage Quantity: ").strip()
#             if cancel_check(usage_qty_str, "Option Creation"):
#                 return
            
#             try:
#                 usage_qty = int(usage_qty_str)
#                 if usage_qty < 0:
#                     print("❌ Usage quantity cannot be negative")
#                     continue
#                 break
#             except ValueError:
#                 print("❌ Usage quantity must be a number")
    
#     try:
#         option_id = db_create_option(o_category_id, option_name, price_adjust, ingredient_id, usage_qty)
#         print(f"✅ Option created with ID: {option_id}")
#         return option_id
#     except Exception as e:
#         print(f"❌ Error: {e}")


def ui_create_option_rule(brand_id, product_id):
    """UI：建立商品選項規則"""
    print("\n=== Create Product Option Rule ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        o_category_id_str = input("Option Category ID: ").strip()
        if cancel_check(o_category_id_str, "Rule Creation"):
            return
        
        try:
            o_category_id = int(o_category_id_str)
            break
        except ValueError:
            print("❌ Category ID must be a number")
    
    while True:
        min_select_str = input("Minimum select (e.g., 0): ").strip()
        max_select_str = input("Maximum select (e.g., 1): ").strip()
        if cancel_check(min_select_str, "Rule Creation") or cancel_check(max_select_str, "Rule Creation"):
            return
        
        if validate_select_range(min_select_str, max_select_str):
            min_select = int(min_select_str)
            max_select = int(max_select_str)
            break
    
    default_option_id = input("Default Option ID (optional, press enter to skip): ").strip() or None
    if default_option_id:
        try:
            default_option_id = int(default_option_id)
        except ValueError:
            print("❌ Default option ID must be a number")
            return
    
    try:
        row = db_create_brand_product_option_rule(
            brand_id, product_id, o_category_id, min_select, max_select, default_option_id
        )
        print(f"✅ Option rule created successfully")
        return row
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_create_option_mutex(brand_id, product_id):
    """UI：建立選項互斥規則"""
    print("\n=== Create Option Mutex Rule ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        option_id_1_str = input("First Option ID: ").strip()
        if cancel_check(option_id_1_str, "Mutex Creation"):
            return
        
        try:
            option_id_1 = int(option_id_1_str)
            break
        except ValueError:
            print("❌ Option ID must be a number")
    
    while True:
        option_id_2_str = input("Second Option ID: ").strip()
        if cancel_check(option_id_2_str, "Mutex Creation"):
            return
        
        try:
            option_id_2 = int(option_id_2_str)
            break
        except ValueError:
            print("❌ Option ID must be a number")
    
    # 確保 low < high
    option_id_low = min(option_id_1, option_id_2)
    option_id_high = max(option_id_1, option_id_2)
    
    if option_id_low == option_id_high:
        print("❌ Option IDs must be different")
        return
    
    print("\nMutex Logic:")
    print("1. EXCLUDE - These options cannot be selected together")
    print("2. REQUIRE_TOGETHER - These options must be selected together")
    
    while True:
        mutex_logic_choice = input("Choose logic (1 or 2): ").strip()
        if cancel_check(mutex_logic_choice, "Mutex Creation"):
            return
        
        if mutex_logic_choice == "1":
            mutex_logic = "EXCLUDE"
            break
        elif mutex_logic_choice == "2":
            mutex_logic = "REQUIRE_TOGETHER"
            break
        else:
            print("❌ Please enter 1 or 2")
    
    try:
        row = db_create_brand_product_option_mutex(
            brand_id, product_id, option_id_low, option_id_high, mutex_logic
        )
        print(f"✅ Mutex rule created successfully")
        return row
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_create_store_option(store_id):
    """UI：設定門市選項"""
    print("\n=== Add Option to Store ===")
    print("(Type ':q' to cancel)\n")
    
    while True:
        option_id_str = input("Option ID: ").strip()
        if cancel_check(option_id_str, "Store Option Creation"):
            return
        
        try:
            option_id = int(option_id_str)
            break
        except ValueError:
            print("❌ Option ID must be a number")
    
    is_enabled = input("Enable this option? (y/n, default y): ").strip().lower() or "y"
    is_enabled = is_enabled == 'y'
    
    try:
        row = db_create_store_option(store_id, option_id, is_enabled)
        status = "enabled" if is_enabled else "disabled"
        print(f"✅ Option {status} for store {store_id}")
        return row
    except Exception as e:
        print(f"❌ Error: {e}")