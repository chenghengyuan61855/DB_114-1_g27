# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.option.manage import (
    db_update_option_category,
    db_update_option,
    db_update_brand_product_option_rule,
    db_update_store_option,
    db_delete_option_category,
    db_delete_option,
    db_delete_brand_product_option_rule,
    db_delete_brand_product_option_mutex,
    db_delete_store_option
)
from ui.helper import cancel_check
from ui.option.helper import (
    validate_category_name,
    validate_option_name,
    validate_price_adjust,
    validate_select_range
)


def ui_update_option_category(o_category_id):
    """UI：更新選項分類"""
    print("\n=== Update Option Category ===")
    print("(Type ':q' to cancel)\n")
    
    new_name = input("New Category Name (press enter to skip): ").strip() or None
    new_order = input("New Display Order (press enter to skip): ").strip() or None
    
    updates = {}
    
    if new_name:
        if not validate_category_name(new_name):
            return
        updates["o_category_name"] = new_name
    
    if new_order:
        if cancel_check(new_order, "Update"):
            return
        try:
            updates["display_order"] = int(new_order)
        except ValueError:
            print("❌ Display order must be a number")
            return
    
    if not updates:
        print("❌ No fields to update")
        return
    
    try:
        db_update_option_category(o_category_id, **updates)
        print(f"✅ Category updated successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_update_option(option_id):
    """UI：更新選項"""
    print("\n=== Update Option ===")
    print("(Type ':q' to cancel)\n")
    
    new_name = input("New Option Name (press enter to skip): ").strip() or None
    new_price_str = input("New Price Adjustment (press enter to skip): ").strip() or None
    
    updates = {}
    
    if new_name:
        if not validate_option_name(new_name):
            return
        updates["option_name"] = new_name
    
    if new_price_str:
        if not validate_price_adjust(new_price_str):
            return
        updates["price_adjust"] = int(new_price_str)
    
    if not updates:
        print("❌ No fields to update")
        return
    
    try:
        db_update_option(option_id, **updates)
        print(f"✅ Option updated successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_update_option_rule(brand_id, product_id, o_category_id):
    """UI：更新商品選項規則"""
    print("\n=== Update Option Rule ===")
    print("(Type ':q' to cancel)\n")
    
    min_select_str = input("New Minimum Select (press enter to skip): ").strip() or None
    max_select_str = input("New Maximum Select (press enter to skip): ").strip() or None
    
    updates = {}
    
    if min_select_str or max_select_str:
        min_val = min_select_str or "0"
        max_val = max_select_str or "0"
        
        if not validate_select_range(min_val, max_val):
            return
        
        if min_select_str:
            updates["min_select"] = int(min_select_str)
        if max_select_str:
            updates["max_select"] = int(max_select_str)
    
    default_option_str = input("New Default Option ID (press enter to skip): ").strip() or None
    if default_option_str:
        try:
            updates["default_option_id"] = int(default_option_str)
        except ValueError:
            print("❌ Default option ID must be a number")
            return
    
    if not updates:
        print("❌ No fields to update")
        return
    
    try:
        db_update_brand_product_option_rule(brand_id, product_id, o_category_id, **updates)
        print(f"✅ Rule updated successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_update_store_option_status(store_id, option_id):
    """UI：更新門市選項狀態"""
    print("\n=== Update Store Option Status ===\n")
    
    print("Current status options:")
    print("1. Enable")
    print("2. Disable")
    
    choice = input("Choose (1 or 2): ").strip()
    
    if choice == "1":
        is_enabled = True
        status = "enabled"
    elif choice == "2":
        is_enabled = False
        status = "disabled"
    else:
        print("❌ Invalid choice")
        return
    
    try:
        db_update_store_option(store_id, option_id, is_enabled)
        print(f"✅ Option {status} for store {store_id}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_delete_option_category(o_category_id):
    """UI：刪除選項分類"""
    print("\n=== Delete Option Category ===\n")
    
    confirm = input(f"Are you sure you want to delete category {o_category_id}? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Deletion cancelled")
        return
    
    try:
        db_delete_option_category(o_category_id)
        print(f"✅ Category deleted successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_delete_option(option_id):
    """UI：刪除選項"""
    print("\n=== Delete Option ===\n")
    
    confirm = input(f"Are you sure you want to delete option {option_id}? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Deletion cancelled")
        return
    
    try:
        db_delete_option(option_id)
        print(f"✅ Option deleted successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_delete_option_rule(brand_id, product_id, o_category_id):
    """UI：刪除商品選項規則"""
    print("\n=== Delete Option Rule ===\n")
    
    confirm = input(f"Are you sure you want to delete the rule for product {product_id}, category {o_category_id}? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Deletion cancelled")
        return
    
    try:
        db_delete_brand_product_option_rule(brand_id, product_id, o_category_id)
        print(f"✅ Rule deleted successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_delete_option_mutex(mutex_id):
    """UI：刪除互斥選項規則"""
    print("\n=== Delete Mutex Rule ===\n")
    
    confirm = input(f"Are you sure you want to delete mutex rule {mutex_id}? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Deletion cancelled")
        return
    
    try:
        db_delete_brand_product_option_mutex(mutex_id)
        print(f"✅ Mutex rule deleted successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_delete_store_option(store_id, option_id):
    """UI：刪除門市選項設定"""
    print("\n=== Delete Store Option ===\n")
    
    confirm = input(f"Are you sure you want to remove option {option_id} from store {store_id}? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Deletion cancelled")
        return
    
    try:
        db_delete_store_option(store_id, option_id)
        print(f"✅ Store option deleted successfully")
    except Exception as e:
        print(f"❌ Error: {e}")