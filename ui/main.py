from ui.user.login import ui_login_user
from ui.user.create import ui_create_user
from menu.main_menu import main_menu
from ui.helper import clear_screen

def run():
    """登入/註冊選單"""
    while True:
        clear_screen()  # ← 每次迴圈開始時清屏
        
        print("Welcome to daTEAbase 🍹")
        print("=====================")
        print("1. 登入 Login")
        print("2. 註冊 Create User")
        print("   （此處只能註冊一般使用者）")
        print("q. Quit")
        print("=====================")
        
        command = input("Enter command: ").strip()
        
        if command == "1":
            user_id = ui_login_user()
            if user_id:
                main_menu(user_id)
                # ← 從 main_menu 返回後，會自動清屏並重新顯示選單
        
        elif command == "2":
            ui_create_user()
            input("\n按 Enter 繼續...")  # ← 讓用戶看完註冊結果
            # ← 返回後會自動清屏
        
        elif command == "q":
            clear_screen()
            print("Goodbye!")
            return
        
        else:
            print("❌ Invalid command. Please try again.")
            input("\n按 Enter 繼續...")  # ← 讓用戶看到錯誤訊息
            # ← 返回後會自動清屏