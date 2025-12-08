from ui.helper import clear_screen
from ui.brand.manage import ui_view_brand_info, ui_update_brand_info
from ui.store.manage import (
    ui_view_brand_stores,
    ui_view_store_detail,
    ui_create_store,
    ui_update_store_info,
    ui_delete_store
)
from ui.store.hours import (
    ui_view_store_hours,
    ui_update_store_hours,
    ui_batch_update_store_hours
)


def brand_info_menu(user_id, brand_id):
    """品牌資訊管理選單"""
    
    while True:
        clear_screen()
        print("\n=== 品牌資訊管理 ===\n")
        print("1. 查看品牌資訊")
        print("2. 更新品牌資訊")
        print("3. 新增品牌")  # ← 新增這一行
        print("q. 返回上一層")
        print("="*30)
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            ui_view_brand_info(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            ui_update_brand_info(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "3":  # ← 新增這個區塊
            ui_create_brand()
            input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")


def store_management_menu(user_id, brand_id):
    """門市管理選單"""
    
    while True:
        clear_screen()
        print("\n=== 門市管理 ===\n")
        print("1. 查看所有門市")
        print("2. 查看門市詳細資訊")
        print("3. 新增門市")
        print("4. 更新門市資訊")
        print("5. 刪除門市")
        print("6. 管理門市營業時間")
        print("q. 返回上一層")
        print("="*30)
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            ui_view_brand_stores(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            store_id = input("請輸入門市 ID: ").strip()
            try:
                ui_view_store_detail(int(store_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的門市 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "3":
            ui_create_store(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "4":
            stores = ui_view_brand_stores(brand_id)
            if stores:
                store_id = input("\n請輸入要更新的門市 ID: ").strip()
                try:
                    ui_update_store_info(int(store_id))
                    input("\n按 Enter 繼續...")
                except ValueError:
                    print("❌ 無效的門市 ID")
                    input("\n按 Enter 繼續...")
        
        elif command == "5":
            stores = ui_view_brand_stores(brand_id)
            if stores:
                store_id = input("\n請輸入要刪除的門市 ID: ").strip()
                try:
                    ui_delete_store(int(store_id))
                    input("\n按 Enter 繼續...")
                except ValueError:
                    print("❌ 無效的門市 ID")
                    input("\n按 Enter 繼續...")
        
        elif command == "6":
            store_hours_menu(brand_id)
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")


def store_hours_menu(brand_id):
    """門市營業時間管理選單"""
    
    while True:
        clear_screen()
        print("\n=== 門市營業時間管理 ===\n")
        
        # 先顯示門市列表
        from ui.store.manage import ui_view_brand_stores
        stores = ui_view_brand_stores(brand_id)
        
        if not stores:
            print("\n目前沒有門市")
            input("\n按 Enter 返回...")
            return
        
        print("\n請選擇操作：")
        print("1. 查看營業時間")
        print("2. 更新營業時間（單日）")
        print("3. 批次更新營業時間（全週）")
        print("q. 返回上一層")
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            store_id = input("請輸入門市 ID: ").strip()
            try:
                ui_view_store_hours(int(store_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的門市 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "2":
            store_id = input("請輸入門市 ID: ").strip()
            try:
                ui_update_store_hours(int(store_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的門市 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "3":
            store_id = input("請輸入門市 ID: ").strip()
            try:
                ui_batch_update_store_hours(int(store_id))
                input("\n按 Enter 繼續...")
            except ValueError:
                print("❌ 無效的門市 ID")
                input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")
