from menu.profile_menu import profile_menu

def main_menu(user_id):
    print(f"Welcome User {user_id} to the Main Menu!")
    while True:
        print("=====================")
        print("1. Profile")
        print("2. Place An Order")
        print("q. Logout")
        command = input("Enter command: ").strip()
        if command == "1":
            profile_menu(user_id)
        elif command == "2":
            #TODO: Implement order placement menu
            print("Order placement menu is under construction.")
        elif command == "q":
            print("Logging out...")
            return

            