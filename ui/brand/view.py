from db.brand.manage import db_fetch_brand_info
from ui.helper import clear_screen

def ui_view_brand_info_readonly(brand_id):
    """查看品牌資訊（只讀，所有人都可以看）"""
    clear_screen()
    print("\n=== 品牌資訊 ===\n")
    
    try:
        brand = db_fetch_brand_info(brand_id)
        
        if not brand:
            print("❌ 品牌不存在")
            return
        
        print(f"品牌名稱：{brand['brand_name']}")
        print(f"品牌地址：{brand['brand_address'] or '（未設定）'}")
        print(f"品牌電話：{brand['brand_phone'] or '（未設定）'}")
        print(f"品牌 Email：{brand['brand_email'] or '（未設定）'}")
        print(f"營業狀態：{'✅ 營業中' if brand['is_active'] else '❌ 已停業'}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
