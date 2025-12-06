# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

def validate_category_name(name: str) -> bool:
    """驗證選項分類名稱"""
    if not name or len(name) > 50:
        print("❌ Category name must be 1-50 characters.")
        return False
    return True


def validate_option_name(name: str) -> bool:
    """驗證選項名稱"""
    if not name or len(name) > 50:
        print("❌ Option name must be 1-50 characters.")
        return False
    return True


def validate_price_adjust(price_str: str) -> bool:
    """驗證價格調整值"""
    try:
        price = int(price_str)
        if price < -1000 or price > 1000:
            print("❌ Price adjustment must be between -1000 and 1000.")
            return False
        return True
    except ValueError:
        print("❌ Price adjustment must be a valid integer.")
        return False


def validate_select_range(min_select_str: str, max_select_str: str) -> bool:
    """驗證選擇數量範圍"""
    try:
        min_select = int(min_select_str)
        max_select = int(max_select_str)
        
        if min_select < 0 or max_select < 0:
            print("❌ Min and max select cannot be negative.")
            return False
        
        if min_select > max_select:
            print("❌ Min select cannot be greater than max select.")
            return False
        
        return True
    except ValueError:
        print("❌ Min and max select must be valid integers.")
        return False