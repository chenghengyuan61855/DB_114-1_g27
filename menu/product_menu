from ui.product.create import ui_create_product, ui_create_store_product
from ui.product.fetch import ui_view_products, ui_view_store_products
from ui.helper import clear_screen

def product_menu(brand_id, store_id):
    """商品管理選單"""
    while True:
        clear_screen()
        
        print("\n=== 商品管理選單 ===")
        print("1. 建立商品")
        print("2. 新增商品到門市")
        print("3. 查看所有商品")
        print("4. 查看門市商品")
        print("q. 返回主選單")
        
        command = input("請輸入指令: ").strip()
        
        if command == "1":
            ui_create_product(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            ui_create_store_product(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "3":
            ui_view_products(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "4":
            ui_view_store_products(store_id)
            input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令，請重新輸入。")
            input("\n按 Enter 繼續...")