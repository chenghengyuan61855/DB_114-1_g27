from db.crud import selective_fetch
from db.order_rating.rate import insert_order_rating
from db.order.fetch import db_fetch_order_status
from ui.order_rating.helper import rating_input
from ui.order_rating.rate_order_item import ui_rate_order_item
from ui.helper import cancel_check, clear_screen

def ui_rate_order(order_id):
    """讓使用者為訂單評分並留下評論"""
    clear_screen()
    order_status = db_fetch_order_status(order_id)
    if order_status != "completed":
        print("Order not completed yet. Cannot rate the order.")
        return

    print("\n=== Rate your order ===")
    print("Type ':q' to cancel rating at any time.\n")

    rating = rating_input("Order Rating")
    if cancel_check(rating, "Order Rating"):
        return ":q"
     
    comment = input("You may leave a comment (optional, leave blank and press Enter to skip): ").strip()
    
    try:
        insert_order_rating(order_id, rating, comment)
        print("Thank you for your rating!")
        print("Do you want to rate individual items in your order? (y/n)")
        order_item_rated = False
        while True:
            choice = input().strip().lower()
            if choice == 'y':
                order_items = selective_fetch("ORDER_ITEM", ['order_item_id'], {"order_id": order_id})
                for item in order_items:
                    decision = ui_rate_order_item(item[0])
                    if decision == ":q":
                        break
                    order_item_rated = True
                if order_item_rated:
                    print("Thank you for rating your order items!")
                break
            elif choice == 'n' or choice == ':q':
                break
            else:
                print("Please enter 'y' or 'n'.")
    except Exception as e:
        print(f"❌ Failed to submit rating: {e}")