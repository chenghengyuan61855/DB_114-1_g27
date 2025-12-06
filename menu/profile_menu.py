from ui.user.profile import ui_view_user_profile, ui_update_user_profile

def profile_menu(user_id):
    while True:
        print("=====================")
        print("1. View Profile")
        print("2. Update Profile")
        print("b. Back to Main Menu")
        command = input("Enter command: ").strip()
        if command == "1":
            ui_view_user_profile(user_id)
        elif command == "2":
            ui_update_user_profile(user_id)
        elif command == "b":
            return
        else:
            print("Invalid command. Please try again.")