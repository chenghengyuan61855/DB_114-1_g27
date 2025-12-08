def cancel_check(input_str: str, ui_type: str) -> bool:
    if input_str.strip() == ":q":
        print(f"{ui_type} cancelled.")
        return True
    return False


def validate_label(label: str) -> bool:
    """驗證標籤名稱（例如地址標籤）
    
    規則：
    - 不能為空
    - 不能為 'q' 或 'Q'（避免與退出指令衝突）
    - 長度不超過 20 字元
    
    Returns:
        bool: 是否通過驗證
    """
    if not label:
        print("❌ 標籤不能為空")
        return False
    
    if label.lower() == 'q':
        print("❌ 標籤不能為 'q'，請使用其他名稱")
        return False
    
    if len(label) > 20:
        print("❌ 標籤長度不能超過 20 字元")
        return False
    
    return True


# 店家管理：保護商品名稱與價格的正確性
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






# 讓前端更好看
import os

def clear_screen():
    """根據作業系統清空終端機畫面。"""
    # 判斷作業系統
    if os.name == 'posix':  # Linux and macOS
        os.system('clear')
    else:  # Windows
        os.system('cls')