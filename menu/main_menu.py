from menu.profile_menu import profile_menu
from menu.option_menu import option_menu
from menu.product_menu import product_menu
from db.user.fetch import db_fetch_user_role
from ui.helper import clear_screen
from ui.order.place_order import ui_place_order
from ui.order.manage import ui_view_user_orders, ui_cancel_order
from ui.order_rating.rate_order import ui_rate_order 
from menu.brand_manager_menu import brand_manager_menu
from menu.store_staff_menu import store_staff_menu  # ← 新增
from db.crud import selective_fetch


#def main_menu(user_id):
   # """主選單（根據用戶角色決定流程）"""
    #print(f"\nWelcome User {user_id}!")
    #input("\n按 Enter 繼續...")
    
    #roles = db_fetch_user_role(user_id)
    #is_manager = any(role in ['brand_manager', 'store_manager'] for role in roles)
    
    #if is_manager:
       # mode_selection_menu(user_id)
   # else:
        #customer_menu(user_id)
        
def main_menu(user_id):
    """主選單（根據用戶角色決定流程）"""
    print(f"\nWelcome User {user_id}!")
    input("\n按 Enter 繼續...")
    
    roles = db_fetch_user_role(user_id)
    
    # 區分三種角色
    is_brand_manager = 'brand_manager' in roles
    is_store_manager = 'store_manager' in roles
    is_store_staff = 'store_staff' in roles
    
    # Brand Manager 有專屬介面
    if is_brand_manager:
        brand_id = get_user_brand_id(user_id)
        if brand_id:
            brand_manager_mode_menu(user_id, brand_id)
        else:
            print("❌ 無法取得品牌資訊")
            input("\n按 Enter 繼續...")
    elif is_store_manager or is_store_staff:
        store_id = get_user_store_id(user_id)  # ← 新增：取得門市 ID
        if store_id:
            store_staff_mode_menu(user_id, store_id)  # ← 新增：門市人員專屬介面
        else:
            print("❌ 無法取得門市資訊")
            input("\n按 Enter 繼續...")
    else:
        customer_menu(user_id)

def get_user_store_id(user_id):
    """取得用戶的門市 ID"""
    rows = selective_fetch(
        "USER_ROLE_ASSIGNMENT",
        ["store_id"],
        {"user_id": user_id, "scope_type": "store"}
    )
    return rows[0][0] if rows else None

def store_staff_mode_menu(user_id, store_id):
    """門市人員模式選擇"""
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("=== 歡迎，門市人員 ===".center(60))
        print("="*60)
        print(f"User ID: {user_id} | Store ID: {store_id}")
        print("="*60)
        print("\n1. 顧客模式（點餐、查看訂單）")
        print("2. 門市管理模式（訂單管理、選項啟用）⭐")
        print("q. 登出")
        print("="*60)
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            customer_menu(user_id)
        elif command == "2":
            store_staff_menu(user_id, store_id)
        elif command == "q":
            print("登出中...")
            input("\n按 Enter 繼續...")
            return
        else:
            print("❌ 無效的指令，請重新輸入")
            input("\n按 Enter 繼續...")


def mode_selection_menu(user_id):
    """管理者模式選擇（顧客模式 or 管理模式）"""
    while True:
        clear_screen()
        print("=====================")
        print("=== 請選擇使用模式 ===")
        print("1. 顧客模式（點餐、查看訂單）")
        print("2. 管理模式（選項管理、商品管理）")
        print("q. 登出")
        print("=====================")
        
        command = input("請輸入指令: ").strip()
        
        if command == "1":
            customer_menu(user_id)
        elif command == "2":
            manager_menu(user_id)
        elif command == "q":
            print("登出中...")
            input("\n按 Enter 繼續...")
            return
        else:
            print("❌ 無效的指令，請重新輸入")
            input("\n按 Enter 繼續...")


def customer_menu(user_id):
    """顧客介面（一般使用者和管理者都能使用）"""
    while True:
        clear_screen()
        # print("=====================")
        print("====== 顧客介面 ======")
        print("1. 個人資料")
        print("2. 開始點餐")
        print("3. 查看我的訂單")
        print("4. 取消訂單")
        print("5. 查看評價紀錄")
        print("q. 返回上一層")
        print("=====================")
        
        command = input("請輸入指令: ").strip()
        
        if command == "1":
            profile_menu(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            # ✅ 點餐功能已實作
            ui_place_order(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "3":
            # ✅ 訂單查詢已實作
            ui_view_user_orders(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "4":
            # ✅ 取消訂單已實作
            ui_cancel_order(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "5":
            ui_rate_order(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令，請重新輸入")
            input("\n按 Enter 繼續...")


def manager_menu(user_id):
    """管理介面（僅限品牌/門市管理者）"""
    brand_id = 1  # TODO: 從資料庫查詢該用戶的品牌 ID
    store_id = 1  # TODO: 從資料庫查詢該用戶的門市 ID

    while True:
        clear_screen()
        print("\n=====================")
        print("=== 管理介面 ===")
        print("1. 個人資料")
        print("2. 選項管理")  # ← 已實作
        print("3. 商品管理")  # ← 部分實作
        print("4. 訂單管理")  # ← 未實作
        print("q. 返回上一層")
        print("=====================")
        
        command = input("請輸入指令: ").strip()
        
        if command == "1":
            profile_menu(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            # ✅ 選項管理已實作
            option_menu(brand_id, store_id)
        
        elif command == "3":
            # ⚠️ 商品管理部分實作（需要建立選單）
            product_menu(brand_id, store_id)
        
        elif command == "4":
            # ❌ 訂單管理尚未實作
            print("⚠️ 訂單管理功能尚未實作")
            input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令，請重新輸入")
            input("\n按 Enter 繼續...")
            
def get_user_brand_id(user_id):
    """取得用戶的品牌 ID"""
    try:
        assignments = selective_fetch(
            "USER_ROLE_ASSIGNMENT",
            ["brand_id"],
            {"user_id": user_id, "scope_type": "brand", "is_active": True}
        )
        if assignments and assignments[0][0]:
            return assignments[0][0]
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def brand_manager_mode_menu(user_id, brand_id):
    """品牌管理者模式選擇"""
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("=== 歡迎，品牌管理者 ===".center(60))
        print("="*60)
        print(f"User ID: {user_id} | Brand ID: {brand_id}")
        print("="*60)
        print("\n1. 顧客模式（點餐、查看訂單）")
        print("2. 品牌管理模式（客製化、評價、商品管理）⭐")
        print("q. 登出")
        print("="*60)
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            customer_menu(user_id)
        elif command == "2":
            brand_manager_menu(user_id, brand_id)
        elif command == "q":
            print("登出中...")
            input("\n按 Enter 繼續...")
            return
        else:
            print("❌ 無效的指令，請重新輸入")
            input("\n按 Enter 繼續...")
