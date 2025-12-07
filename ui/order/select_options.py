from db.order.fetch import db_fetch_available_option_list, db_fetch_option_rule, db_fetch_option_category_list
from db.crud import selective_fetch  # ← 新增導入
from ui.helper import cancel_check, clear_screen
from ui.order.helper import go_back_check


def ui_select_options_in_category(brand_id, store_id, product_id, o_category_id):
    """在某個選項分類中選擇選項
    
    Args:
        brand_id: 品牌 ID
        store_id: 門市 ID
        product_id: 商品 ID
        o_category_id: 選項分類 ID
    
    Returns:
        tuple: (option_ids, option_price) 或 ([], 0) 或 (None, None) 或 (":b", ":b")
    """
    from db.order.fetch import db_fetch_available_option_list, db_fetch_option_rule
    from db.crud import selective_fetch
    from ui.helper import cancel_check
    from ui.order.helper import go_back_check
    
    enabled_options = db_fetch_available_option_list(store_id, o_category_id)
    
    if not enabled_options:
        print("No options available in this category.")
        return [], 0
    
    category = db_fetch_option_rule(brand_id, product_id, o_category_id)
    
    # 查詢分類名稱
    category_data = selective_fetch(
        "OPTION_CATEGORY", 
        ["o_category_name"], 
        {"o_category_id": o_category_id}
    )
    category_name = category_data[0][0] if category_data else "Unknown"
    
    min_s = category.get("min_select", 0)
    max_s = category.get("max_select", 0)
    
    print(f"\n--- Option Category: {category_name} ---")
    
    if min_s == 0 and max_s == 0:
        print("No options need to be selected in this category.")
        return [], 0
    
    # ✅ 修正：根據 min_s 調整提示訊息
    if min_s == 0:
        print(f"Please select up to {max_s} option(s) (press Enter to skip):")
    else:
        print(f"Please select {min_s} to {max_s} option(s):")
    
    for option in enabled_options:
        option_id, option_name, price_adjust = option
        print(f"- {option_id}: {option_name} (+${price_adjust})")
    
    while True:
        choice = input("Choose option(s) (comma-separated for multiple): ").strip()
        
        if cancel_check(choice, "Option selection"):
            return None, None
        
        if go_back_check(choice):
            return ":b", ":b"
        
        # ✅ 修正：允許空輸入（當 min_s = 0 時）
        if choice == "":
            if min_s == 0:
                print("No options selected.")
                return [], 0
            else:
                print(f"❌ Please select at least {min_s} option(s).")
                continue
        
        try:
            selected_ids = [int(x.strip()) for x in choice.split(',')]
        except ValueError:
            print("❌ Invalid input. Please enter option IDs separated by commas.")
            continue
        
        # ✅ 驗證選擇數量
        if len(selected_ids) < min_s or len(selected_ids) > max_s:
            if min_s == 0:
                print(f"❌ Please select up to {max_s} option(s).")
            else:
                print(f"❌ Please select {min_s} to {max_s} option(s).")
            continue
        
        # ✅ 驗證 option_id 是否有效
        valid_ids = {opt[0] for opt in enabled_options}
        if not all(sid in valid_ids for sid in selected_ids):
            print("❌ Invalid option ID(s).")
            continue
        
        # ✅ 計算總價
        total_price = sum(
            opt[2] for opt in enabled_options if opt[0] in selected_ids
        )
        
        return selected_ids, total_price


def ui_select_options(brand_id, store_id, product_id):
    """選擇所有選項分類
    
    Args:
        brand_id: 品牌 ID
        store_id: 門市 ID
        product_id: 商品 ID
    
    Returns:
        tuple: (all_options, total_option_price) 或 (None, None) 或 (":b", ":b")
    """
    from db.order.fetch import db_fetch_option_category_list
    
    categories = db_fetch_option_category_list(brand_id)
    
    if not categories:
        print("No option categories available for this product.")
        return {}, 0
    
    all_options = {}
    total_option_price = 0
    
    for o_category_id, category_name in categories:
        # ✅ 傳入 brand_id
        result = ui_select_options_in_category(brand_id, store_id, product_id, o_category_id)
        
        if result == (None, None):
            return None, None
        
        if result == (":b", ":b"):
            return ":b", ":b"
        
        option_ids, option_price = result
        
        if not option_ids:
            continue
        
        all_options[category_name] = option_ids
        total_option_price += option_price
    
    return all_options, total_option_price