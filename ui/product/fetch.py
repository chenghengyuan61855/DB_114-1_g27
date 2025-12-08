# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

from db.product.fetch import db_fetch_product, db_fetch_store_product
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

def ui_view_products(brand_id=None):
    """UI：查看商品列表"""
    try:
        products = db_fetch_product(brand_id=brand_id)
        if not products:
            print("No products found.")
            return
        
        print("\n=== Product List ===")
        for p in products:
            print(f"\nID: {p['product_id']} | Name: {p['product_name']}")
            print(f"  Size: {p['size'] or 'N/A'}")
            print(f"  Description: {p['product_description'] or 'N/A'}")
            print(f"  Active: {p['is_active']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_store_products(store_id):
    """UI：查看門市販售的商品（含商品名稱）"""
    try:
        # 1. 取得門市商品列表
        store_products = db_fetch_store_product(store_id=store_id)
        if not store_products:
            print("No products found for this store.")
            return
        
        # 2. 取得所有商品 ID
        product_ids = [sp['product_id'] for sp in store_products]
        
        # 3. 批次查詢商品資訊
        products_detail = fetch_in("PRODUCT", "product_id", product_ids, "product_id")
        
        # 4. 建立 product_id -> product_name 的對應
        product_map = {p[0]: p[2] for p in products_detail}  # {product_id: product_name}
        
        # 5. 顯示門市商品列表（使用中文對齊）
        print(f"\n=== Store {store_id} - Products ===")
        print(f"{pad_string('商品ID', 12)}{pad_string('商品名稱', 24)}{pad_string('價格', 12)}{pad_string('狀態', 12)}")
        print("="*60)
        
        for sp in store_products:
            product_id = sp['product_id']
            product_name = product_map.get(product_id, "Unknown")
            price = sp['price']
            status = "✅ 啟用" if sp['is_active'] else "❌ 停用"
            
            product_id_str = str(product_id)
            price_str = f"${price}"
            
            print(f"{pad_string(product_id_str, 12)}{pad_string(product_name, 24)}{pad_string(price_str, 12)}{pad_string(status, 12)}")
    
    except Exception as e:
        print(f"❌ Error: {e}")