from ui.helper import clear_screen
from ui.option.fetch import ui_view_store_options
from ui.option.rule_manage import ui_update_store_option_status
from ui.product.fetch import ui_view_store_products
from ui.product.manage import ui_update_store_product_status
from ui.order.manage import (
    ui_view_pending_orders,
    ui_view_accepted_orders,
    ui_view_history_orders
)

def store_staff_menu(user_id, store_id):
    """門市人員主選單"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("=== 門市管理介面 ===".center(60))
        print("="*60)
        print(f"Store ID: {store_id} | User ID: {user_id}")
        print("="*60)
        
        print("\n【訂單管理】")
        print("1. 查看待處理訂單（可接受/拒絕）")
        print("2. 查看進行中訂單（可完成）")
        print("3. 查看歷史訂單")
        
        print("\n【門市設定】")
        print("4. 查看門市商品")
        print("5. 啟用/停用門市商品")
        print("6. 查看門市選項設定")
        print("7. 啟用/停用門市選項")
        
        print("\n【其他】")
        print("q. 返回上一層")
        print("="*60)
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            ui_view_pending_orders(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            ui_view_accepted_orders(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "3":
            ui_view_history_orders(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "4":
            ui_view_store_products(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "5":
            ui_update_store_product_status(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "6":
            ui_view_store_options(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "7":
            ui_update_store_option_status(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "q" or command == "Q":
            print("👋 登出成功！")
            return
        
        else:
            print("❌ 無效指令，請重新選擇")
            input("\n按 Enter 繼續...")