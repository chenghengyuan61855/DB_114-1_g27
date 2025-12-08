# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

from db.product.manage import db_update_store_product_status
from ui.product.fetch import ui_view_store_products  # ← 新增

def ui_update_store_product_status(store_id, product_id=None):
    """UI：更新門市商品狀態
    
    Args:
        store_id: 門市 ID（必填）
        product_id: 商品 ID（可選，如果不提供則先顯示可選列表）
    """
    # ✅ 修正：先顯示該門市的所有商品
    if product_id is None:
        print("\n=== Update Store Product Status ===\n")
        print(f"門市 {store_id} 的商品列表：\n")
        ui_view_store_products(store_id)
        
        product_id_str = input("\n請輸入要修改的商品 ID (輸入 'q' 取消): ").strip()
        
        if product_id_str.lower() == 'q':
            print("❌ 操作已取消")
            return
        
        try:
            product_id = int(product_id_str)
        except ValueError:
            print("❌ 無效的商品 ID")
            return
    
    # ✅ 防護：確認該商品屬於此門市
    from db.product.fetch import db_fetch_store_product
    store_product = db_fetch_store_product(store_id=store_id, product_id=product_id)
    
    if not store_product:
        print(f"❌ 錯誤：門市 {store_id} 沒有商品 {product_id}")
        return
    
    current_status = "啟用" if store_product[0]['is_active'] else "停用"
    print(f"\n目前狀態：{current_status}")
    print("\n請選擇新狀態：")
    print("1. 啟用 (Enable)")
    print("2. 停用 (Disable)")
    
    choice = input("選擇 (1 or 2): ").strip()
    
    if choice == "1":
        is_active = True
        status = "enabled"
    elif choice == "2":
        is_active = False
        status = "disabled"
    else:
        print("❌ Invalid choice")
        return
    
    try:
        db_update_store_product_status(store_id, product_id, is_active)
        print(f"✅ 商品 {product_id} 已成功設為 {status}")
    except Exception as e:
        print(f"❌ Error: {e}")