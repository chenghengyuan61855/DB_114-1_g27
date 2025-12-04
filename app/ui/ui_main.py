from app.ui.ui_user import ui_login_user, ui_create_user

def run():
    print("Welcome to DaTeabase 🍹")
    print("=====================")
    print("1. Login")
    print("2. Create User")
    print("q. Quit")
    while True:
        command = input("Enter command: ").strip()
        if command == "1":
            user_id = ui_login_user()
            # TODO: go to menu.main_menu.py if login successful
        elif command == "2":
            ui_create_user()
        elif command == "q":
            print("Goodbye!")
            return
        else:
            print("Invalid command. Please try again.")