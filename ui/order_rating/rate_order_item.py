from db.order_rating.rate import insert_order_item_rating
from ui.helper import cancel_check
from ui.order_rating.helper import rating_input, show_order_item_details

def ui_rate_order_item(order_item_id):
    """讓使用者為訂單項目評分並留下評論"""
    print("\n=== Rate your order item ===")
    print("Type ':q' to cancel rating at any time.\n")

    if not show_order_item_details(order_item_id):
        return "continue"
    
    rating = rating_input("Order Item Rating")
    if cancel_check(rating, "Order Item Rating"):
        return ":q"
     
    comment = input("You may leave a comment (optional, leave blank and press Enter to skip): ").strip()
    
    try:
        insert_order_item_rating(order_item_id, rating, comment)
        print("Thank you for your rating!")
    except Exception as e:
        print(f"❌ Failed to submit rating: {e}")
    return "continue"