# menu/brand_manager_menu.py 的修正版本
# ============================
# 整合品牌與門市管理功能
# ============================

from ui.helper import clear_screen
from menu.option_menu import option_menu
from menu.product_menu import product_menu
from menu.brand_store_menu import brand_info_menu, store_management_menu  # ← 新增
from db.crud import selective_fetch
from ui.rating.brand_manager_rating import (
    ui_view_all_ratings,
    ui_view_product_ratings,
    ui_view_low_rated_products,
    ui_view_rating_statistics
)


def get_user_name(user_id):
    """取得使用者名稱"""
    try:
        result = selective_fetch(
            "APP_USER",
            ["user_name"],
            {"user_id": user_id}
        )
        if result and result[0][0]:
            return result[0][0]
        return f"User {user_id}"
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"User {user_id}"


def get_brand_name(brand_id):
    """取得品牌名稱"""
    try:
        result = selective_fetch(
            "BRAND",
            ["brand_name"],
            {"brand_id": brand_id}
        )
        if result and result[0][0]:
            return result[0][0]
        return f"Brand {brand_id}"
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Brand {brand_id}"


def brand_manager_menu(user_id, brand_id):
    """品牌管理者主選單"""
    user_name = get_user_name(user_id)
    brand_name = get_brand_name(brand_id)
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("=== 品牌管理者介面 ===".center(60))
        print("="*60)
        print(f"Manager: {user_name} | Brand: {brand_name}")
        print("="*60)
        
        print("\n【品牌與門市管理】")  # ← 新增區塊
        print("1. 品牌資訊管理 🏢")
        print("2. 門市管理 🏪")
        
        print("\n【商品與選項管理】")
        print("3. 商品管理")
        print("4. 選項分類管理（甜度、冰塊、加料等）")
        print("5. 選項管理（全糖、去冰、珍珠等）")
        print("6. 商品客製化規則設定 ⭐")
        print("7. 選項互斥邏輯設定 ⭐")
        
        print("\n【評價系統】")
        print("8. 查看所有評價")
        print("9. 查看特定商品評價")
        print("10. 查看低分商品（< 3 星）")
        print("11. 評價統計分析")
        
        print("\n【其他】")
        print("q. 登出 (Logout)")
        print("="*60)
        
        command = input("\n請輸入指令: ").strip()
        
        # ✅ 新增：品牌與門市管理
        if command == "1":
            brand_info_menu(user_id, brand_id)
        
        elif command == "2":
            store_management_menu(user_id, brand_id)
        
        # 商品與選項管理（編號往後移）
        elif command == "3":
            product_menu(brand_id, store_id=None)
        
        elif command == "4":
            option_category_submenu(brand_id)
        
        elif command == "5":
            option_submenu(brand_id)
        
        elif command == "6":
            product_option_rule_submenu(brand_id)
        
        elif command == "7":
            product_option_mutex_submenu(brand_id)
        
        # 評價系統（編號往後移）
        elif command == "8":
            ui_view_all_ratings(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "9":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_view_product_ratings(int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "10":
            ui_view_low_rated_products(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "11":
            ui_view_rating_statistics(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令，請重新輸入")
            input("\n按 Enter 繼續...")


# ===== 以下是原有的子選單函式（不變）=====

def option_category_submenu(brand_id):
    """選項分類子選單"""
    from ui.option.create import ui_create_option_category
    from ui.option.fetch import ui_view_option_categories
    from ui.option.rule_manage import ui_update_option_category, ui_delete_option_category
    
    while True:
        clear_screen()
        print("\n=== 選項分類管理 ===")
        print("1. 建立選項分類")
        print("2. 查看所有分類")
        print("3. 更新選項分類")
        print("4. 刪除選項分類")
        print("q. 返回上一層")
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            ui_create_option_category(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            ui_view_option_categories(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "3":
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_update_option_category(int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的分類 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "4":
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_delete_option_category(int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的分類 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")


def option_submenu(brand_id):
    """選項子選單"""
    from ui.option.create import ui_create_option
    from ui.option.fetch import ui_view_options
    from ui.option.rule_manage import ui_update_option, ui_delete_option
    
    while True:
        clear_screen()
        print("\n=== 選項管理 ===")
        print("1. 建立選項")
        print("2. 查看所有選項")
        print("3. 更新選項")
        print("4. 刪除選項")
        print("q. 返回上一層")
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_create_option(int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的分類 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "2":
            o_category_id = input("請輸入選項分類 ID（留空查看全部）: ").strip()
            try:
                if o_category_id:
                    ui_view_options(int(o_category_id))
                else:
                    ui_view_options()
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的分類 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "3":
            option_id = input("請輸入選項 ID: ").strip()
            try:
                ui_update_option(int(option_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的選項 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "4":
            option_id = input("請輸入選項 ID: ").strip()
            try:
                ui_delete_option(int(option_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的選項 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")


def product_option_rule_submenu(brand_id):
    """商品客製化規則子選單"""
    from ui.option.create import ui_create_option_rule
    from ui.option.fetch import ui_view_product_option_rules
    from ui.option.rule_manage import ui_update_option_rule, ui_delete_option_rule
    
    while True:
        clear_screen()
        print("\n=== 商品客製化規則管理 ⭐ ===")
        print("功能說明：設定商品可使用哪些選項群組，以及選擇數量限制")
        print("範例：珍珠奶茶必須選擇 1 個甜度、1 個冰塊、0-3 個配料")
        print()
        print("1. 建立規則（新增選項群組到商品）")
        print("2. 查看商品的所有規則")
        print("3. 更新規則（修改選擇數量限制）")
        print("4. 刪除規則")
        print("q. 返回上一層")
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_create_option_rule(brand_id, int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "2":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_view_product_option_rules(int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "3":
            product_id = input("請輸入商品 ID: ").strip()
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_update_option_rule(brand_id, int(product_id), int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "4":
            product_id = input("請輸入商品 ID: ").strip()
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_delete_option_rule(brand_id, int(product_id), int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")


def product_option_mutex_submenu(brand_id):
    """選項互斥邏輯子選單"""
    from ui.option.create import ui_create_option_mutex
    from ui.option.fetch import ui_view_product_option_mutex
    from ui.option.rule_manage import ui_delete_option_mutex
    
    while True:
        clear_screen()
        print("\n=== 選項互斥邏輯管理 ⭐ ===")
        print("功能說明：設定哪些選項不能同時選擇")
        print("範例：熱飲 vs 去冰、全糖 vs 無糖")
        print()
        print("1. 建立互斥規則")
        print("2. 查看商品的互斥規則")
        print("3. 刪除互斥規則")
        print("q. 返回上一層")
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_create_option_mutex(brand_id, int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "2":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_view_product_option_mutex(int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "3":
            mutex_id = input("請輸入互斥規則 ID: ").strip()
            try:
                ui_delete_option_mutex(int(mutex_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的互斥規則 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")
