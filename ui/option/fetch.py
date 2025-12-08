# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

from db.option.fetch import (
    db_fetch_option_category,
    db_fetch_option,
    db_fetch_brand_product_option_rule,
    db_fetch_brand_product_option_mutex,
    db_fetch_store_option
)
from db.crud import fetch_in  # ← 新增

# 中文對齊輔助函數
def get_display_width(text):
    """計算字串顯示寬度（中文字算2個字元，英文算1個）"""
    width = 0
    for char in str(text):
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f':
            width += 2
        else:
            width += 1
    return width

def pad_string(text, target_width):
    """將字串填充到指定顯示寬度"""
    current_width = get_display_width(text)
    padding = target_width - current_width
    return text + ' ' * max(0, padding)

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
            print(f"Category {rule['o_category_id']}: select {rule['min_select']}-{rule['max_select']}")
            if rule['default_option_id']:
                print(f"  Default: {rule['default_option_id']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_product_option_mutex(product_id):
    """UI：查看商品的互斥選項規則"""
    try:
        mutex_rules = db_fetch_brand_product_option_mutex(product_id=product_id)
        if not mutex_rules:
            print(f"✅ 商品 {product_id} 沒有設定互斥規則")
            return
        
        print(f"\n=== 商品 {product_id} - 互斥規則 ===\n")
        
        # 查詢所有相關的選項名稱
        from db.crud import fetch_in
        option_ids = set()
        for rule in mutex_rules:
            option_ids.add(rule['option_id_low'])
            if rule['option_id_high']:
                option_ids.add(rule['option_id_high'])
        
        options_detail = fetch_in("OPTION", "option_id", list(option_ids), "option_id")
        option_map = {o[0]: o[2] for o in options_detail}  # {option_id: option_name}
        
        for idx, rule in enumerate(mutex_rules, 1):
            option_low_name = option_map.get(rule['option_id_low'], f"ID {rule['option_id_low']}")
            
            print(f"{idx}. 互斥規則 ID: {rule['mutex_id']}")
            
            if rule['mutex_logic'] == 'exclusive' and rule['option_id_high']:
                option_high_name = option_map.get(rule['option_id_high'], f"ID {rule['option_id_high']}")
                print(f"   規則：「{option_low_name}」和「{option_high_name}」不能同時選擇")
                print(f"   選項 ID: {rule['option_id_low']} ⚔️ {rule['option_id_high']}")
            elif rule['mutex_logic'] == 'single':
                print(f"   規則：「{option_low_name}」只能單選")
                print(f"   選項 ID: {rule['option_id_low']}")
            else:
                print(f"   規則類型：{rule['mutex_logic']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_store_options(store_id):
    """UI：查看門市選項設定（含選項名稱）"""
    try:
        # 1. 取得門市選項列表
        store_options = db_fetch_store_option(store_id=store_id)
        if not store_options:
            print(f"No options configured for store {store_id}.")
            return
        
        # 2. 取得所有選項 ID
        option_ids = [so['option_id'] for so in store_options]
        
        # 3. 批次查詢選項資訊
        options_detail = fetch_in("OPTION", "option_id", option_ids, "option_id")
        
        # 4. 建立 option_id -> option_name 的對應
        option_map = {o[0]: o[2] for o in options_detail}  # {option_id: option_name}
        
        # 5. 顯示門市選項列表（使用中文對齊）
        print(f"\n=== Store {store_id} - Options ===")
        print(f"{pad_string('選項ID', 12)}{pad_string('選項名稱', 24)}{pad_string('狀態', 12)}")
        print("="*48)
        
        for so in store_options:
            option_id = so['option_id']
            option_name = option_map.get(option_id, "Unknown")
            status = "✅ 啟用" if so['is_enabled'] else "❌ 停用"
            
            option_id_str = str(option_id)
            
            print(f"{pad_string(option_id_str, 12)}{pad_string(option_name, 24)}{pad_string(status, 12)}")
    
    except Exception as e:
        print(f"❌ Error: {e}")