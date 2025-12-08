# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

from db.user.address import (
    db_fetch_user_addresses,
    db_create_user_address,
    db_update_user_address,
    db_delete_user_address
)
from ui.helper import clear_screen, cancel_check, validate_label

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


def ui_view_user_addresses(user_id):
    """查看使用者地址列表"""
    clear_screen()
    print("\n=== 我的地址 ===\n")
    
    addresses = db_fetch_user_addresses(user_id)
    
    if not addresses:
        print("目前沒有儲存的地址")
        return addresses
    
    print(f"{pad_string('標籤', 16)}{pad_string('行政區', 16)}{pad_string('詳細地址', 50)}")
    print("="*90)
    
    for addr in addresses:
        label_str = addr['label']
        district_str = addr['district']
        address_str = addr['address']
        
        print(f"{pad_string(label_str, 16)}{pad_string(district_str, 16)}{pad_string(address_str, 50)}")
    
    return addresses


def ui_create_user_address(user_id):
    """新增使用者地址"""
    clear_screen()
    print("\n=== 新增地址 ===\n")
    print("(輸入 ':q' 可取消操作)\n")
    
    # 輸入標籤
    while True:
        label = input("地址標籤（例如：家、公司）: ").strip()
        if cancel_check(label, "新增地址"):
            return
        if validate_label(label):
            break
    
    # 輸入行政區
    while True:
        district = input("行政區（例如：大安區、中正區）: ").strip()
        if cancel_check(district, "新增地址"):
            return
        if district:
            break
        print("❌ 行政區不能為空")
    
    # 輸入詳細地址
    while True:
        address = input("詳細地址: ").strip()
        if cancel_check(address, "新增地址"):
            return
        if address:
            break
        print("❌ 地址不能為空")
    
    # 確認
    print(f"\n確認新增地址：")
    print(f"  標籤：{label}")
    print(f"  行政區：{district}")
    print(f"  詳細地址：{address}")
    
    confirm = input("\n確認新增？(y/n): ").strip().lower()
    
    if confirm == 'y':
        try:
            success = db_create_user_address(user_id, district, label, address)
            if success:
                print(f"✅ 地址新增成功")
            else:
                print(f"❌ 地址新增失敗")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ 操作已取消")


def ui_update_user_address(user_id):
    """更新使用者地址"""
    addresses = ui_view_user_addresses(user_id)
    
    if not addresses:
        return
    
    label = input("\n請輸入要修改的地址標籤 (輸入 'q' 取消): ").strip()
    
    if label.lower() == 'q':
        print("❌ 操作已取消")
        return
    
    # 找到對應的地址
    target_addr = None
    for addr in addresses:
        if addr['label'] == label:
            target_addr = addr
            break
    
    if not target_addr:
        print("❌ 找不到該地址")
        return
    
    print(f"\n目前資訊：")
    print(f"  標籤：{target_addr['label']}")
    print(f"  行政區：{target_addr['district']}")
    print(f"  詳細地址：{target_addr['address']}")
    print("\n(輸入新值以修改，留空則保持不變，輸入 ':q' 取消操作)\n")
    
    # 輸入新標籤
    new_label = input(f"新標籤 [{target_addr['label']}]: ").strip()
    if cancel_check(new_label, "修改地址"):
        return
    
    # 檢查新標籤（如果有輸入的話）
    if new_label and not validate_label(new_label):
        return
    
    # 輸入新行政區
    new_district = input(f"新行政區 [{target_addr['district']}]: ").strip()
    if cancel_check(new_district, "修改地址"):
        return
    if not new_district:
        new_district = target_addr['district']
    
    # 輸入新地址
    new_address = input(f"新地址 [{target_addr['address']}]: ").strip()
    if cancel_check(new_address, "修改地址"):
        return
    if not new_address:
        new_address = target_addr['address']
    
    updates = {}
    
    # 如果要更新標籤
    if new_label and new_label != target_addr['label']:
        updates["new_label"] = new_label
    
    # 如果要更新行政區
    if new_district != target_addr['district']:
        updates["district"] = new_district
    
    # 如果要更新地址
    if new_address != target_addr['address']:
        updates["address"] = new_address
    
    if not updates:
        print("❌ 沒有任何修改")
        return
    
    try:
        db_update_user_address(user_id, label, **updates)
        print("✅ 地址更新成功")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_delete_user_address(user_id):
    """刪除使用者地址"""
    addresses = ui_view_user_addresses(user_id)
    
    if not addresses:
        return
    
    label = input("\n請輸入要刪除的地址標籤 (輸入 'q' 取消): ").strip()
    
    if label.lower() == 'q':
        print("❌ 操作已取消")
        return
    
    # 確認刪除
    confirm = input(f"\n確認刪除地址「{label}」？(y/n): ").strip().lower()
    
    if confirm == 'y':
        try:
            db_delete_user_address(user_id, label)
            print("✅ 地址刪除成功")
        except ValueError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ 操作已取消")


def ui_manage_addresses(user_id):
    """地址管理主選單"""
    while True:
        clear_screen()
        print("\n=== 地址管理 ===\n")
        print("1. 查看地址列表")
        print("2. 新增地址")
        print("3. 修改地址")
        print("4. 刪除地址")
        print("q. 返回")
        print("="*30)
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            ui_view_user_addresses(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            ui_create_user_address(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "3":
            ui_update_user_address(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "4":
            ui_delete_user_address(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")
