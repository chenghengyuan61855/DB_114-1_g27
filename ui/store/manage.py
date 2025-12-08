from db.store.manage import (
    db_fetch_brand_stores,
    db_fetch_store_info,
    db_create_store,
    db_update_store_info,
    db_delete_store
)
from db.store.hours import db_init_store_hours
from ui.helper import clear_screen, cancel_check

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


def ui_view_brand_stores(brand_id):
    """查看品牌下的所有門市"""
    clear_screen()
    print("\n=== 門市列表 ===\n")
    
    try:
        stores = db_fetch_brand_stores(brand_id)
        
        if not stores:
            print("目前沒有門市")
            return stores
        
        print(f"{pad_string('門市ID', 12)}{pad_string('門市名稱', 24)}{pad_string('電話', 20)}{pad_string('狀態', 12)}{pad_string('接單', 12)}")
        print("="*80)
        
        for store in stores:
            store_id_str = str(store['store_id'])
            store_name = store['store_name']
            phone = store['store_phone'] or "未設定"
            status = "✅ 營業中" if store['is_active'] else "❌ 已停業"
            accepting = "✅ 接單中" if store['is_accepting_orders'] else "❌ 停止接單"
            
            print(f"{pad_string(store_id_str, 12)}{pad_string(store_name, 24)}{pad_string(phone, 20)}{pad_string(status, 12)}{pad_string(accepting, 12)}")
        
        return stores
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def ui_view_store_detail(store_id):
    """查看門市詳細資訊"""
    clear_screen()
    print("\n=== 門市詳細資訊 ===\n")
    
    try:
        store = db_fetch_store_info(store_id)
        
        if not store:
            print("❌ 門市不存在")
            return
        
        print(f"門市 ID：{store['store_id']}")
        print(f"品牌 ID：{store['brand_id']}")
        print(f"門市名稱：{store['store_name']}")
        print(f"門市地址：{store['store_address'] or '（未設定）'}")
        print(f"門市電話：{store['store_phone'] or '（未設定）'}")
        print(f"營業狀態：{'✅ 營業中' if store['is_active'] else '❌ 已停業'}")
        print(f"接單狀態：{'✅ 接單中' if store['is_accepting_orders'] else '❌ 停止接單'}")
        print(f"外送服務：{'✅ 提供外送' if store['is_accepting_deliveries'] else '❌ 不提供外送'}")
        
        if store['min_order_qty']:
            print(f"最低訂購數量：{store['min_order_qty']} 杯")
        
        if store['min_order_total_price']:
            print(f"外送最低金額：${store['min_order_total_price']}")
        
        print(f"建立時間：{store['created_at']}")
        print(f"更新時間：{store['updated_at']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_create_store(brand_id):
    """新增門市"""
    clear_screen()
    print("\n=== 新增門市 ===\n")
    print("(輸入 ':q' 取消操作)\n")
    
    try:
        # 門市名稱
        while True:
            store_name = input("門市名稱（必填，例如：台北公館店）: ").strip()
            if cancel_check(store_name, "新增門市"):
                return
            
            if not store_name:
                print("❌ 門市名稱不能為空")
                continue
            
            if len(store_name) > 20:
                print("❌ 門市名稱不能超過 20 個字元")
                continue
            
            break
        
        # 門市地址
        store_address = input("門市地址（可選）: ").strip()
        if cancel_check(store_address, "新增門市"):
            return
        if not store_address:
            store_address = None
        
        # 門市電話
        store_phone = input("門市電話（可選）: ").strip()
        if cancel_check(store_phone, "新增門市"):
            return
        if not store_phone:
            store_phone = None
        
        # 確認新增
        print("\n確認新增門市：")
        print(f"門市名稱：{store_name}")
        print(f"門市地址：{store_address or '（未設定）'}")
        print(f"門市電話：{store_phone or '（未設定）'}")
        
        confirm = input("\n確認新增？(y/n): ").strip().lower()
        
        if confirm == 'y':
            store_id = db_create_store(brand_id, store_name, store_address, store_phone)
            print(f"\n✅ 門市新增成功（門市 ID: {store_id}）")
            
            # 詢問是否初始化營業時間
            init_hours = input("\n是否初始化營業時間（預設 10:00-22:00）？(y/n): ").strip().lower()
            if init_hours == 'y':
                count = db_init_store_hours(store_id)
                print(f"✅ 營業時間初始化完成（{count} 天）")
        else:
            print("❌ 操作已取消")
    
    except ValueError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_update_store_info(store_id):
    """更新門市資訊"""
    clear_screen()
    print("\n=== 更新門市資訊 ===\n")
    print("(留空則保持不變，輸入 ':q' 取消操作)\n")
    
    try:
        # 先顯示目前資訊
        store = db_fetch_store_info(store_id)
        
        if not store:
            print("❌ 門市不存在")
            return
        
        print("目前資訊：")
        print(f"門市名稱：{store['store_name']}")
        print(f"門市地址：{store['store_address'] or '（未設定）'}")
        print(f"門市電話：{store['store_phone'] or '（未設定）'}")
        print(f"營業狀態：{'✅ 營業中' if store['is_active'] else '❌ 已停業'}")
        print(f"接單狀態：{'✅ 接單中' if store['is_accepting_orders'] else '❌ 停止接單'}")
        print()
        
        updates = {}
        
        # 門市名稱
        new_name = input(f"新門市名稱 [{store['store_name']}]: ").strip()
        if cancel_check(new_name, "更新門市資訊"):
            return
        if new_name:
            if len(new_name) > 20:
                print("❌ 門市名稱不能超過 20 個字元")
                return
            updates["store_name"] = new_name
        
        # 門市地址
        new_address = input(f"新門市地址 [{store['store_address'] or ''}]: ").strip()
        if cancel_check(new_address, "更新門市資訊"):
            return
        if new_address:
            updates["store_address"] = new_address
        
        # 門市電話
        new_phone = input(f"新門市電話 [{store['store_phone'] or ''}]: ").strip()
        if cancel_check(new_phone, "更新門市資訊"):
            return
        if new_phone:
            updates["store_phone"] = new_phone
        
        # 營業狀態
        print(f"\n營業狀態 [目前：{'營業中' if store['is_active'] else '已停業'}]")
        print("1. 營業中")
        print("2. 已停業")
        status_choice = input("選擇（留空不變）: ").strip()
        if cancel_check(status_choice, "更新門市資訊"):
            return
        if status_choice == "1":
            updates["is_active"] = True
        elif status_choice == "2":
            updates["is_active"] = False
        
        # 接單狀態
        print(f"\n接單狀態 [目前：{'接單中' if store['is_accepting_orders'] else '停止接單'}]")
        print("1. 接單中")
        print("2. 停止接單")
        order_choice = input("選擇（留空不變）: ").strip()
        if cancel_check(order_choice, "更新門市資訊"):
            return
        if order_choice == "1":
            updates["is_accepting_orders"] = True
        elif order_choice == "2":
            updates["is_accepting_orders"] = False
        
        # 如果沒有要更新的欄位
        if not updates:
            print("⚠️ 沒有要更新的欄位")
            return
        
        # 確認更新
        print("\n確認更新以下資訊：")
        for key, value in updates.items():
            field_name = {
                "store_name": "門市名稱",
                "store_address": "門市地址",
                "store_phone": "門市電話",
                "is_active": "營業狀態",
                "is_accepting_orders": "接單狀態"
            }.get(key, key)
            
            if isinstance(value, bool):
                value_str = "是" if value else "否"
            else:
                value_str = value
            
            print(f"  {field_name}：{value_str}")
        
        confirm = input("\n確認更新？(y/n): ").strip().lower()
        
        if confirm == 'y':
            db_update_store_info(store_id, **updates)
            print("\n✅ 門市資訊更新成功")
        else:
            print("❌ 操作已取消")
    
    except ValueError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_delete_store(store_id):
    """刪除門市（軟刪除）"""
    clear_screen()
    print("\n=== 刪除門市 ===\n")
    
    try:
        # 先顯示門市資訊
        store = db_fetch_store_info(store_id)
        
        if not store:
            print("❌ 門市不存在")
            return
        
        print(f"門市名稱：{store['store_name']}")
        print(f"門市地址：{store['store_address'] or '（未設定）'}")
        
        # 確認刪除
        print("\n⚠️ 注意：刪除門市後將無法恢復（軟刪除，資料仍保留）")
        confirm = input(f"\n確認刪除門市「{store['store_name']}」？(y/n): ").strip().lower()
        
        if confirm == 'y':
            db_delete_store(store_id)
            print("\n✅ 門市刪除成功")
        else:
            print("❌ 操作已取消")
    
    except Exception as e:
        print(f"❌ Error: {e}")
