

def order_menu(user_id):
    print(f"Welcome User {user_id} to the Order Menu!")
    while True:
        print("=====================")
        print("1. Place An Order")
        print("2. View Order History")
        print("b. Back to Main Menu")
        command = input("Enter command: ").strip()
        if command == "1":
            #TODO ui_place_order(user_id)
            pass
        elif command == "2":
            #TODO ui_view_order_history(user_id)
            pass
        elif command == "b":
            return