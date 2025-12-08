# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

# update by YUAN: nagivate to order_rating 

from db.order.manage import (
    db_fetch_pending_orders,
    db_fetch_accepted_orders,
    db_fetch_history_orders,
    db_accept_order,
    db_reject_order,
    db_complete_order,
    db_cancel_order,
    db_fetch_user_orders
)
from db.order.fetch import db_fetch_order_details
from ui.helper import clear_screen
from ui.order_rating.rate_order import ui_rate_order

# 中文對齊輔助函數
def get_display_width(text):
    """計算字串顯示寬度（中文字算2個字元，英文算1個）"""
    width = 0
    for char in str(text):
        # 判斷是否為中文字符（包括中文標點符號）
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

def ui_view_pending_orders(store_id):
    """查看待處理訂單（含詳情）並可直接接受/拒絕"""
    clear_screen()
    print(f"\n{'='*80}")
    print(f"門市 {store_id} - 待處理訂單".center(80))
    print(f"{'='*80}\n")
    
    orders = db_fetch_pending_orders(store_id)
    
    if not orders:
        print("✅ 目前沒有待處理訂單")
        return
    
    # 顯示所有待處理訂單的詳細內容
    for idx, order in enumerate(orders, 1):
        print(f"\n{'─'*80}")
        print(f"訂單Order ID: {order['order_id']}")
        print(f"{'─'*80}")
        
        # 獲取訂單詳情
        details = db_fetch_order_details(order['order_id'])
        if not details:
            print("❌ 無法獲取訂單詳情")
            continue
        
        order_info = details['order_info']
        items = details['items']
        
        # 顯示訂單基本資訊
        order_type = "外送" if order_info['order_type'] == 'delivery' else "自取"
        print(f"訂單類型：{order_type}")
        print(f"下單時間：{str(order_info['placed_at'])[:19]}")
        print(f"付款方式：{order_info['payment_method']}")
        
        if order_info['order_type'] == 'delivery':
            print(f"收件人：{order_info['receiver_name']} ({order_info['receiver_phone']})")
            print(f"地址：{order_info['delivery_address']}")
        
        # 顯示訂單明細
        print(f"\n訂單內容：")
        for item in items:
            print(f"  • {item['product_name']} x {item['qty']} - ${item['unit_price']}")
            if item['options']:
                option_names = [opt['option_name'] for opt in item['options']]
                print(f"    ({', '.join(option_names)}) +${item['option_total_adjust']}")
            print(f"    小計：${item['line_total_price']}")
        
        print(f"\n訂單總額：${order_info['total_price']}")
    
    print(f"\n{'='*80}\n")
    
    # 詢問是否要處理訂單
    while True:
        action = input("請選擇操作：[a]接受訂單 / [r]拒絕訂單 / [q]返回：").strip().lower()
        
        if action == 'q':
            return
        
        elif action == 'a':
            order_id = input("請輸入要接受的訂單 ID: ").strip()
            try:
                order_id_int = int(order_id)
                # 驗證訂單是否在待處理列表中
                if order_id_int not in [o['order_id'] for o in orders]:
                    print("❌ 無效的訂單 ID")
                    continue
                
                db_accept_order(order_id_int)
                print(f"✅ 訂單 {order_id} 已接受")
                return
            except ValueError:
                print("❌ 無效的訂單 ID")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif action == 'r':
            order_id = input("請輸入要拒絕的訂單 ID: ").strip()
            try:
                order_id_int = int(order_id)
                # 驗證訂單是否在待處理列表中
                if order_id_int not in [o['order_id'] for o in orders]:
                    print("❌ 無效的訂單 ID")
                    continue
                
                reason = input("請輸入拒絕原因: ").strip()
                if not reason:
                    print("❌ 拒絕原因不能為空")
                    continue
                
                db_reject_order(order_id_int, reason)
                print(f"✅ 訂單 {order_id} 已拒絕，原因：{reason}")
                return
            except ValueError:
                print("❌ 無效的訂單 ID")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        else:
            print("❌ 無效的指令")


def ui_view_accepted_orders(store_id):
    """查看進行中的訂單（已接受但未完成）"""
    clear_screen()
    print(f"\n{'='*80}")
    print(f"門市 {store_id} - 進行中訂單".center(80))
    print(f"{'='*80}\n")
    
    orders = db_fetch_accepted_orders(store_id)
    
    if not orders:
        print("✅ 目前沒有進行中的訂單")
        return
    
    # 使用中文對齊
    print(f"{pad_string('訂單ID', 12)}{pad_string('訂單類型', 16)}{pad_string('接受時間', 24)}{pad_string('金額', 12)}")
    print("="*64)
    
    for order in orders:
        order_type = "外送" if order['order_type'] == 'delivery' else "自取"
        order_id_str = str(order['order_id'])
        time_str = str(order['accepted_at'])[:16] if order['accepted_at'] else "N/A"
        price_str = f"${order['total_price']}"
        
        print(f"{pad_string(order_id_str, 12)}{pad_string(order_type, 16)}{pad_string(time_str, 24)}{pad_string(price_str, 12)}")
    
    print(f"\n{'='*64}\n")
    
    # 詢問是否要完成訂單
    while True:
        action = input("請選擇操作：[c]完成訂單 / [v]查看詳情 / [q]返回：").strip().lower()
        
        if action == 'q':
            return
        
        elif action == 'c':
            order_id = input("請輸入要完成的訂單 ID: ").strip()
            try:
                order_id_int = int(order_id)
                # 驗證訂單是否在進行中列表
                if order_id_int not in [o['order_id'] for o in orders]:
                    print("❌ 無效的訂單 ID")
                    continue
                
                db_complete_order(order_id_int)
                print(f"✅ 訂單 {order_id} 已完成")
                return
            except ValueError:
                print("❌ 無效的訂單 ID")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif action == 'v':
            order_id = input("請輸入要查看的訂單 ID: ").strip()
            try:
                ui_view_order_details(int(order_id), store_id)
                input("\n按 Enter 返回列表...")
                # 重新顯示列表
                ui_view_accepted_orders(store_id)
                return
            except ValueError:
                print("❌ 無效的訂單 ID")
        
        else:
            print("❌ 無效的指令")


def ui_view_history_orders(store_id):
    """查看歷史訂單（已完成/已拒絕）"""
    clear_screen()
    print(f"\n{'='*100}")
    print(f"門市 {store_id} - 歷史訂單（最近50筆）".center(100))
    print(f"{'='*100}\n")
    
    orders = db_fetch_history_orders(store_id)
    
    if not orders:
        print("目前沒有歷史訂單")
        return
    
    # 使用中文對齊
    print(f"{pad_string('訂單ID', 12)}{pad_string('狀態', 16)}{pad_string('訂單類型', 16)}{pad_string('下單時間', 24)}{pad_string('金額', 12)}{pad_string('備註', 20)}")
    print("="*100)
    
    for order in orders:
        status_map = {
            'completed': '已完成',
            'rejected': '已拒絕',
            'cancelled': '已取消'
        }
        order_type = "外送" if order['order_type'] == 'delivery' else "自取"
        status = status_map.get(order['order_status'], order['order_status'])
        
        order_id_str = str(order['order_id'])
        time_str = str(order['placed_at'])[:16]
        price_str = f"${order['total_price']}"
        note = order['rejected_reason'] if order['rejected_reason'] else ""
        
        print(f"{pad_string(order_id_str, 12)}{pad_string(status, 16)}{pad_string(order_type, 16)}{pad_string(time_str, 24)}{pad_string(price_str, 12)}{pad_string(note, 20)}")
    
    print(f"\n{'='*100}\n")
    
    # 詢問是否要查看詳情
    order_id = input("請輸入要查看的訂單 ID (按 Enter 返回): ").strip()
    
    if order_id:
        try:
            ui_view_order_details(int(order_id), store_id)
        except ValueError:
            print("❌ 無效的訂單 ID")


def ui_view_order_details(order_id, store_id=None):
    """查看訂單詳細內容
    
    Args:
        order_id: 訂單 ID
        store_id: 門市 ID（如果提供，會驗證訂單是否屬於該門市）
    """
    clear_screen()
    print(f"\n=== 訂單詳情 (Order ID: {order_id}) ===\n")
    
    details = db_fetch_order_details(order_id)
    
    if not details:
        print("❌ 訂單不存在")
        return
    
    order_info = details['order_info']
    
    # ✅ 驗證訂單是否屬於該門市
    if store_id and order_info['store_id'] != store_id:
        print("❌ 此訂單不屬於您的門市")
        return
    
    items = details['items']
    
    # 顯示訂單基本資訊
    print("【訂單資訊】")
    print(f"訂單狀態：{order_info['order_status']}")
    print(f"訂單類型：{'外送' if order_info['order_type'] == 'delivery' else '自取'}")
    print(f"下單時間：{order_info['placed_at']}")
    print(f"付款方式：{order_info['payment_method']}")
    
    if order_info['order_type'] == 'delivery':
        print(f"\n【外送資訊】")
        print(f"收件人：{order_info['receiver_name']}")
        print(f"電話：{order_info['receiver_phone']}")
        print(f"地址：{order_info['delivery_address']}")
    
    # 顯示訂單明細
    print(f"\n【訂單明細】")
    print("="*80)
    
    for idx, item in enumerate(items, 1):
        print(f"\n{idx}. {item['product_name']} x {item['qty']}")
        print(f"   商品單價：${item['unit_price']}")
        
        if item['options']:
            print(f"   客製化選項：")
            for opt in item['options']:
                price_str = f"+${opt['price_adjust']}" if opt['price_adjust'] > 0 else "免費"
                print(f"     • {opt['option_name']} ({price_str})")
            print(f"   選項加價：${item['option_total_adjust']}")
        else:
            print(f"   客製化選項：無")
        
        print(f"   小計：${item['line_total_price']}")
    
    print(f"\n{'='*80}")
    print(f"訂單總額：${order_info['total_price']}")
    print(f"{'='*80}\n")


def ui_accept_order(store_id):
    """接受訂單"""
    ui_view_pending_orders(store_id)
    
    if not db_fetch_pending_orders(store_id):
        return
    
    order_id = input("\n請輸入要接受的訂單 ID (輸入 'q' 取消): ").strip()
    
    if order_id.lower() == 'q':
        print("❌ 操作已取消")
        return
    
    try:
        order_id_int = int(order_id)
        
        # ✅ 新增：顯示訂單詳情
        ui_view_order_details(order_id_int, store_id)
        
        # 確認接單
        confirm = input("確認接受此訂單？(y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ 操作已取消")
            return
        
        db_accept_order(order_id_int)
        print(f"✅ 訂單 {order_id} 已接受")
    except ValueError:
        print("❌ 無效的訂單 ID")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_reject_order(store_id):
    """拒絕訂單"""
    ui_view_pending_orders(store_id)
    
    if not db_fetch_pending_orders(store_id):
        return
    
    order_id = input("\n請輸入要拒絕的訂單 ID (輸入 'q' 取消): ").strip()
    
    if order_id.lower() == 'q':
        print("❌ 操作已取消")
        return
    
    try:
        order_id_int = int(order_id)
        
        # ✅ 新增：顯示訂單詳情
        ui_view_order_details(order_id_int, store_id)
        
        # 輸入拒絕原因
        reason = input("\n請輸入拒絕原因: ").strip()
        
        if not reason:
            print("❌ 拒絕原因不能為空")
            return
        
        # 確認拒單
        confirm = input(f"確認拒絕此訂單（原因：{reason}）？(y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ 操作已取消")
            return
        
        db_reject_order(order_id_int, reason)
        print(f"✅ 訂單 {order_id} 已拒絕，原因：{reason}")
    except ValueError:
        print("❌ 無效的訂單 ID")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_complete_order(store_id):
    """完成訂單"""
    clear_screen()
    print(f"\n=== 完成訂單 ===\n")
    
    order_id = input("請輸入要完成的訂單 ID (輸入 'q' 取消): ").strip()
    
    if order_id.lower() == 'q':
        print("❌ 操作已取消")
        return
    
    try:
        db_complete_order(int(order_id))
        print(f"✅ 訂單 {order_id} 已完成")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_user_orders(user_id):
    """查看我的訂單"""
    clear_screen()
    print(f"\n=== 我的訂單 ===\n")
    
    orders = db_fetch_user_orders(user_id)
    
    if not orders:
        print("目前沒有訂單記錄")
        return
    
    # 使用中文對齊
    print(f"{pad_string('訂單ID', 12)}{pad_string('門市ID', 12)}{pad_string('狀態', 16)}{pad_string('訂單類型', 16)}{pad_string('下單時間', 24)}{pad_string('金額', 12)}")
    print("="*92)
    
    for order in orders:
        status_map = {
            'placed': '待處理',
            'accepted': '已接受',
            'completed': '已完成',
            'rejected': '已拒絕',
            'cancelled': '已取消'
        }
        order_type = "外送" if order['order_type'] == 'delivery' else "自取"
        status = status_map.get(order['order_status'], order['order_status'])
        
        order_id_str = str(order['order_id'])
        store_id_str = str(order['store_id'])
        time_str = str(order['placed_at'])[:16]
        price_str = f"${order['total_price']}"
        
        print(f"{pad_string(order_id_str, 12)}{pad_string(store_id_str, 12)}{pad_string(status, 16)}{pad_string(order_type, 16)}{pad_string(time_str, 24)}{pad_string(price_str, 12)}")
    
    # 移到迴圈外面，顯示完所有訂單後才詢問
    print("\nEnter order_id to rate an order or leave blank and press Enter to go back:")
    order_id_input = input("Order ID: ").strip()
    if order_id_input == "" or order_id_input == ":b" or order_id_input == ":q":
        return
    try:
        order_id = int(order_id_input)
        ui_rate_order(order_id, user_id)  # 加上 user_id 參數
    except ValueError:
        print("❌ 無效的訂單 ID")
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_cancel_order(user_id):
    """取消訂單"""
    clear_screen()
    print(f"\n=== 取消訂單 ===\n")
    
    # 先顯示使用者的訂單
    orders = db_fetch_user_orders(user_id)
    
    if not orders:
        print("目前沒有訂單記錄")
        return
    
    # 篩選出可以取消的訂單（只有 'placed' 狀態可以取消）
    cancelable_orders = [o for o in orders if o['order_status'] == 'placed']
    
    if not cancelable_orders:
        print("✅ 目前沒有可取消的訂單（只有「待處理」狀態的訂單可以取消）")
        return
    
    print("可取消的訂單：\n")
    print(f"{pad_string('訂單ID', 12)}{pad_string('門市ID', 12)}{pad_string('訂單類型', 16)}{pad_string('下單時間', 24)}{pad_string('金額', 12)}")
    print("="*76)
    
    for order in cancelable_orders:
        order_type = "外送" if order['order_type'] == 'delivery' else "自取"
        order_id_str = str(order['order_id'])
        store_id_str = str(order['store_id'])
        time_str = str(order['placed_at'])[:16]
        price_str = f"${order['total_price']}"
        
        print(f"{pad_string(order_id_str, 12)}{pad_string(store_id_str, 12)}{pad_string(order_type, 16)}{pad_string(time_str, 24)}{pad_string(price_str, 12)}")
    
    order_id = input("\n請輸入要取消的訂單 ID (輸入 'q' 取消操作): ").strip()
    
    if order_id.lower() == 'q':
        print("❌ 操作已取消")
        return
    
    try:
        db_cancel_order(int(order_id), user_id)
        print(f"✅ 訂單 {order_id} 已取消")
    except ValueError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
