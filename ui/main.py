from ui.user.login import ui_login_user
from ui.user.create import ui_create_user
from menu.main_menu import main_menu

def run():
    print("Welcome to daTEAbase 🍹")
    while True:
        print("=====================")
        print("1. Login")
        print("2. Create User")
        print("q. Quit")
        command = input("Enter command: ").strip()
        if command == "1":
            user_id = ui_login_user()
            if user_id:
                main_menu(user_id)
        elif command == "2":
            ui_create_user()
        elif command == "q":
            print("Goodbye!")
            return
        else:
            print("Invalid command. Please try again.")