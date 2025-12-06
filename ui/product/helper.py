# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-06
# ASSISTED BY: Claude
# ============================

def validate_product_name(name: str) -> bool:
    """驗證商品名稱
    
    規則：
    - 長度 1-50 字元
    - 允許中文、英文、數字、空格
    """
    if not name or len(name) > 50:
        print("❌ Product name must be 1-50 characters.")
        return False
    return True


def validate_price(price) -> bool:
    """驗證價格"""
    try:
        price_int = int(price)
        if price_int < 0:
            print("❌ Price cannot be negative.")
            return False
        return True
    except ValueError:
        print("❌ Price must be a valid integer.")
        return False