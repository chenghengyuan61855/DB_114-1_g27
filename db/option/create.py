# db/option/create.py
from db.crud import insert

def db_create_option_category(brand_id, o_category_name, display_order):
    """建立選項群組"""
    row = insert("OPTION_CATEGORY", {
        "brand_id": brand_id,
        "o_category_name": o_category_name,
        "display_order": display_order,
        "is_active": True,
    })
    return row[0]

def db_create_option(o_category_id, option_name, price_adjust, ingredient_id, usage_qty):
    """建立選項"""
    row = insert("OPTION", {
        "o_category_id": o_category_id,
        "option_name": option_name,
        "price_adjust": price_adjust,
        "ingredient_id": ingredient_id,
        "usage_qty": usage_qty,
        "is_active": True,
    })
    return row[0]