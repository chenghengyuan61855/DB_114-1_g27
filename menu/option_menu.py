# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from ui.option.create import (
    ui_create_option_category,
    ui_create_option,
    ui_create_option_rule,
    ui_create_option_mutex,
    ui_create_store_option
)
from ui.option.fetch import (
    ui_view_option_categories,
    ui_view_options,
    ui_view_product_option_rules,
    ui_view_product_option_mutex,
    ui_view_store_options
)
from ui.option.rule_manage import (
    ui_update_option_category,
    ui_update_option,
    ui_update_option_rule,
    ui_update_store_option_status,
    ui_delete_option_category,
    ui_delete_option,
    ui_delete_option_rule,
    ui_delete_option_mutex,
    ui_delete_store_option
)
from ui.helper import clear_screen  # ← 導入 clear_screen


def option_menu(brand_id, store_id):
    """選項管理選單"""
    while True:
        clear_screen()  # ← 清除螢幕內容
        print("\n=== 選項管理選單 ===")
        print("1. 建立選項分類")
        print("2. 建立選項")
        print("3. 建立商品選項規則")
        print("4. 建立選項互斥規則")
        print("5. 新增門市選項")
        print("6. 查看選項分類")
        print("7. 查看選項")
        print("8. 查看商品選項規則")
        print("9. 查看商品選項互斥規則")
        print("10. 查看門市選項")
        print("11. 更新選項分類")
        print("12. 更新選項")
        print("13. 更新選項規則")
        print("14. 更新門市選項狀態")
        print("15. 刪除選項分類")
        print("16. 刪除選項")
        print("17. 刪除選項規則")
        print("18. 刪除互斥規則")
        print("19. 刪除門市選項")
        print("q. 返回主選單")
        
        command = input("請輸入指令: ").strip()
        
        if command == "1":
            ui_create_option_category(brand_id)
            input("\n按 Enter 繼續...")
        elif command == "2":
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_create_option(int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的分類 ID")
                input("\n按 Enter 繼續...")
        elif command == "3":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_create_option_rule(brand_id, int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        elif command == "4":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_create_option_mutex(brand_id, int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        elif command == "5":
            ui_create_store_option(store_id)
            input("\n按 Enter 繼續...")
        elif command == "6":
            ui_view_option_categories(brand_id)
            input("\n按 Enter 繼續...")
        elif command == "7":
            ui_view_options()
            input("\n按 Enter 繼續...")
        elif command == "8":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_view_product_option_rules(int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        elif command == "9":
            product_id = input("請輸入商品 ID: ").strip()
            try:
                ui_view_product_option_mutex(int(product_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的商品 ID")
                input("\n按 Enter 繼續...")
        elif command == "10":
            ui_view_store_options(store_id)
            input("\n按 Enter 繼續...")
        elif command == "11":
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_update_option_category(int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的分類 ID")
                input("\n按 Enter 繼續...")
        elif command == "12":
            option_id = input("請輸入選項 ID: ").strip()
            try:
                ui_update_option(int(option_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的選項 ID")
                input("\n按 Enter 繼續...")
        elif command == "13":
            product_id = input("請輸入商品 ID: ").strip()
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_update_option_rule(brand_id, int(product_id), int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的 ID")
                input("\n按 Enter 繼續...")
        elif command == "14":
            option_id = input("請輸入選項 ID: ").strip()
            try:
                ui_update_store_option_status(store_id, int(option_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的選項 ID")
                input("\n按 Enter 繼續...")
        elif command == "15":
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_delete_option_category(int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的分類 ID")
                input("\n按 Enter 繼續...")
        elif command == "16":
            option_id = input("請輸入選項 ID: ").strip()
            try:
                ui_delete_option(int(option_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的選項 ID")
                input("\n按 Enter 繼續...")
        elif command == "17":
            product_id = input("請輸入商品 ID: ").strip()
            o_category_id = input("請輸入選項分類 ID: ").strip()
            try:
                ui_delete_option_rule(brand_id, int(product_id), int(o_category_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的 ID")
                input("\n按 Enter 繼續...")
        elif command == "18":
            mutex_id = input("請輸入互斥規則 ID: ").strip()
            try:
                ui_delete_option_mutex(int(mutex_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的互斥規則 ID")
                input("\n按 Enter 繼續...")
        elif command == "19":
            option_id = input("請輸入選項 ID: ").strip()
            try:
                ui_delete_store_option(store_id, int(option_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的選項 ID")
                input("\n按 Enter 繼續...")
        elif command == "q":
            return
        else:
            print("❌ 無效的指令，請重新輸入。")
            input("\n按 Enter 繼續...")