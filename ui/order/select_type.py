from ui.helper import cancel_check

def ui_select_order_type():
    print("Select order type:")
    print("1. Pickup")
    print("2. Delivery")

    while True:
        order_type = input("Enter choice (1 or 2): ").strip()

        if cancel_check(order_type, "Order Placement"):
            return None
        
        if order_type == '1':
            return "Pickup"
        elif order_type == '2':
            return "Delivery"
        else:
            print("Invalid choice. Please enter 1 for Pickup or 2 for Delivery.")

    
    