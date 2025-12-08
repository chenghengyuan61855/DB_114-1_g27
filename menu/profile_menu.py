from ui.user.profile import ui_view_user_profile, ui_update_user_profile
from ui.user.address import ui_manage_addresses
from ui.helper import clear_screen

def profile_menu(user_id):
    while True:
        clear_screen()  # ← 每次進入選單前清屏
        
        print("=====================")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. 地址管理")
        print("q. Back to Main Menu")
        
        command = input("Enter command: ").strip()
        
        if command == "1":
            ui_view_user_profile(user_id)
            input("\n按 Enter 繼續...")  # ← 讓用戶看完資料再繼續
            
        elif command == "2":
            ui_update_user_profile(user_id)
            input("\n按 Enter 繼續...")
        
        elif command == "3":
            ui_manage_addresses(user_id)
            input("\n按 Enter 繼續...")
            
        elif command == "q":
            return  # ← 直接返回，上層會自動清屏
        
        else:
            print("Invalid command. Please try again.")
            input("\n按 Enter 繼續...")