from db.crud import selective_fetch
from db.order_rating.rate import insert_order_rating
from db.order_rating.fetch import check_order_rating_exists
from db.order.fetch import db_fetch_order_status, db_verify_order_ownership
from ui.order_rating.helper import rating_input
from ui.order_rating.rate_order_item import ui_rate_order_item
from ui.helper import cancel_check, clear_screen

def ui_rate_order(order_id, user_id):
    """讓使用者為訂單評分並留下評論
    
    Args:
        order_id: 訂單 ID
        user_id: 用戶 ID（用於驗證訂單擁有權）
    """
    clear_screen()
    
    # 驗證訂單擁有權
    if not db_verify_order_ownership(order_id, user_id):
        print("❌ 此訂單不存在或不屬於您")
        return
    
    order_status = db_fetch_order_status(order_id)
    if order_status != "completed":
        print("❌ 訂單尚未完成，無法評價")
        return
    
    # ✅ 檢查是否已經評分過
    if check_order_rating_exists(order_id):
        print("✅ 您已經評價過此訂單")
        print("\n是否要評價訂單中的個別商品？(y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            order_items = selective_fetch("ORDER_ITEM", ['order_item_id'], {"order_id": order_id})
            order_item_rated = False
            for item in order_items:
                decision = ui_rate_order_item(item[0])
                if decision == ":q":
                    break
                order_item_rated = True
            if order_item_rated:
                print("感謝您的評價！")
        return

    print("\n=== Rate your order ===")
    print("Type ':q' to cancel rating at any time.\n")

    rating = rating_input("Order Rating")
    if rating == ":q":
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