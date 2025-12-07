# ============================
# AUTHOR: YUAN, KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from menu.profile_menu import profile_menu
from menu.option_menu import option_menu
from db.user.fetch import db_fetch_user_role

def main_menu(user_id):
    """主選單（根據用戶角色決定流程）"""
    print(f"\nWelcome User {user_id}!")
    
    # 🎯 查詢用戶角色
    roles = db_fetch_user_role(user_id)
    
    # 判斷用戶是否為管理者
    is_manager = any(role in ['brand_manager', 'store_manager'] for role in roles)
    
    if is_manager:
        # 👔 管理者：先讓他選擇模式
        mode_selection_menu(user_id)
    else:
        # 👤 一般顧客：直接進入顧客介面
        customer_menu(user_id)


def mode_selection_menu(user_id):
    """管理者模式選擇（顧客模式 or 管理模式）"""
    while True:
        print("\n=====================")
        print("=== 請選擇使用模式 ===")
        print("1. 顧客模式（點餐、查看訂單）")
        print("2. 管理模式（選項管理、商品管理）")
        print("q. 登出")
        print("=====================")
        
        command = input("請輸入指令: ").strip()
        
        if command == "1":
            customer_menu(user_id)  # ← 進入顧客介面
        
        elif command == "2":
            manager_menu(user_id)   # ← 進入管理介面
        
        elif command == "q":
            print("登出中...")
            return
        
        else:
            print("❌ 無效的指令，請重新輸入")


def customer_menu(user_id):
    """顧客介面（一般使用者和管理者都能使用）"""
    while True:
        print("\n=====================")
        print("=== 顧客介面 ===")
        print("1. 個人資料")
        print("2. 開始點餐")
        print("3. 查看我的訂單")
        print("4. 查看評價紀錄")
        print("q. 返回上一層")
        print("=====================")
        
        command = input("請輸入指令: ").strip()
        
        if command == "1":
            profile_menu(user_id)
        
        elif command == "2":
            print("⚠️ 點餐功能尚未實作")
            # TODO: 呼叫 order_menu(user_id)
        
        elif command == "3":
            print("⚠️ 訂單查詢功能尚未實作")
            # TODO: 呼叫 ui_view_my_orders(user_id)
        
        elif command == "4":
            print("⚠️ 評價查詢功能尚未實作")
            # TODO: 呼叫 ui_view_my_ratings(user_id)
        
        elif command == "q":
            return  # ← 返回上一層（模式選擇 or 登出）
        
        else:
            print("❌ 無效的指令，請重新輸入")


def manager_menu(user_id):
    """管理介面（僅限品牌/門市管理者）"""
    brand_id = 1  # TODO: 從資料庫查詢該用戶的品牌 ID
    store_id = 1  # TODO: 從資料庫查詢該用戶的門市 ID
    
    while True:
        print("\n=====================")
        print("=== 管理介面 ===")
        print("1. 個人資料")
        print("2. 選項管理")
        print("3. 商品管理（未實作）")
        print("4. 訂單管理（未實作）")
        print("q. 返回上一層")
        print("=====================")
        
        command = input("請輸入指令: ").strip()
        
        if command == "1":
            profile_menu(user_id)
        
        elif command == "2":
            option_menu(brand_id, store_id)
        
        elif command == "3":
            print("⚠️ 商品管理功能尚未實作")
        
        elif command == "4":
            print("⚠️ 訂單管理功能尚未實作")
        
        elif command == "q":
            return  # ← 返回模式選擇選單
        
        else:
            print("❌ 無效的指令，請重新輸入")