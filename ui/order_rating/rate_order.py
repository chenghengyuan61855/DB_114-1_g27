from db.crud import selective_fetch
from ui.helper import cancel_check, clear_screen

def rate_order(order_id):
    """讓使用者為訂單評分並留下評論"""
    clear_screen()
    
    print("\n=== 為您的訂單評分 ===")
    
    while True:
        try:
            rating = int(input("請輸入評分（1-5 星）：").strip())
            if rating < 1 or rating > 5:
                print("評分必須在 1 到 5 之間。請再試一次。")
                continue
            break
        except ValueError:
            print("無效的輸入。請輸入數字 1 到 5。")
    
    comment = input("您可以留下評論（可選，按 Enter 跳過）：").strip()
    
    try:
        from db.order_rating.fetch import insert_order_rating
        insert_order_rating(order_id, rating, comment)
        print("感謝您的評分！")
    except Exception as e:
        print(f"❌ 評分提交失敗：{e}")