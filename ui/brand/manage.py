from db.brand.manage import db_fetch_brand_info, db_update_brand_info
from ui.helper import clear_screen, cancel_check

def ui_view_brand_info(brand_id):
    """查看品牌資訊"""
    clear_screen()
    print("\n=== 品牌資訊 ===\n")
    
    try:
        brand = db_fetch_brand_info(brand_id)
        
        if not brand:
            print("❌ 品牌不存在")
            return
        
        print(f"品牌 ID：{brand['brand_id']}")
        print(f"品牌名稱：{brand['brand_name']}")
        print(f"品牌地址：{brand['brand_address'] or '（未設定）'}")
        print(f"品牌電話：{brand['brand_phone'] or '（未設定）'}")
        print(f"品牌 Email：{brand['brand_email'] or '（未設定）'}")
        print(f"啟用狀態：{'✅ 啟用' if brand['is_active'] else '❌ 停用'}")
        print(f"建立時間：{brand['created_at']}")
        print(f"更新時間：{brand['updated_at']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_update_brand_info(brand_id):
    """更新品牌資訊"""
    clear_screen()
    print("\n=== 更新品牌資訊 ===\n")
    print("(留空則保持不變，輸入 ':q' 取消操作)\n")
    
    try:
        # 先顯示目前資訊
        brand = db_fetch_brand_info(brand_id)
        
        if not brand:
            print("❌ 品牌不存在")
            return
        
        print("目前資訊：")
        print(f"品牌名稱：{brand['brand_name']}")
        print(f"品牌地址：{brand['brand_address'] or '（未設定）'}")
        print(f"品牌電話：{brand['brand_phone'] or '（未設定）'}")
        print(f"品牌 Email：{brand['brand_email'] or '（未設定）'}")
        print()
        
        updates = {}
        
        # 品牌名稱
        new_name = input(f"新品牌名稱 [{brand['brand_name']}]: ").strip()
        if cancel_check(new_name, "更新品牌資訊"):
            return
        if new_name:
            if len(new_name) > 20:
                print("❌ 品牌名稱不能超過 20 個字元")
                return
            updates["brand_name"] = new_name
        
        # 品牌地址
        new_address = input(f"新品牌地址 [{brand['brand_address'] or ''}]: ").strip()
        if cancel_check(new_address, "更新品牌資訊"):
            return
        if new_address:
            if len(new_address) > 100:
                print("❌ 品牌地址不能超過 100 個字元")
                return
            updates["brand_address"] = new_address
        
        # 品牌電話
        new_phone = input(f"新品牌電話 [{brand['brand_phone'] or ''}]: ").strip()
        if cancel_check(new_phone, "更新品牌資訊"):
            return
        if new_phone:
            if len(new_phone) > 20:
                print("❌ 品牌電話不能超過 20 個字元")
                return
            updates["brand_phone"] = new_phone
        
        # 品牌 Email
        new_email = input(f"新品牌 Email [{brand['brand_email'] or ''}]: ").strip()
        if cancel_check(new_email, "更新品牌資訊"):
            return
        if new_email:
            if len(new_email) > 50:
                print("❌ Email 不能超過 50 個字元")
                return
            if "@" not in new_email:
                print("❌ Email 格式不正確")
                return
            updates["brand_email"] = new_email
        
        # 如果沒有要更新的欄位
        if not updates:
            print("⚠️ 沒有要更新的欄位")
            return
        
        # 確認更新
        print("\n確認更新以下資訊：")
        for key, value in updates.items():
            field_name = {
                "brand_name": "品牌名稱",
                "brand_address": "品牌地址",
                "brand_phone": "品牌電話",
                "brand_email": "品牌 Email"
            }.get(key, key)
            print(f"  {field_name}：{value}")
        
        confirm = input("\n確認更新？(y/n): ").strip().lower()
        
        if confirm == 'y':
            db_update_brand_info(brand_id, **updates)
            print("\n✅ 品牌資訊更新成功")
        else:
            print("❌ 操作已取消")
    
    except ValueError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
