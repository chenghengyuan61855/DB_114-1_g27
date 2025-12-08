from ui.helper import cancel_check
from db.order_rating.fetch import fetch_order_item_details

def rating_input(context:str):
    """檢查評分輸入是否有效或是否取消"""
    valid_rating = {'1', '2', '3', '4', '5'}
    while True:
        rating_input = input("Please enter a rating (1-5 stars): ").strip()
        if cancel_check(rating_input, context):
            return ":q"
        if rating_input not in valid_rating:
            print("Invalid rating. Please enter a number between 1 and 5.")
            continue
        return int(rating_input)
    
def show_order_item_details(order_item_id):
    """顯示訂單項目詳細資訊
    
    Args:
        order_item_id (int): 訂單項目ID

    Returns:
        bool: 是否成功顯示訂單項目詳細資訊
    """
    main, options, total = fetch_order_item_details(order_item_id)
    if not main:
        print("Unexpected error: Order item not found.")
        return False

    print("\nOrder Item Details:")
    print(f"Item: {main[1]}")
    print(f"Unit Price: ${main[2]}")
    print(f"Quantity: {main[3]}")
    if options:
        print("Options:")
        for option in options:
            print(f" - {option[1]}: ${option[2]}")
    print(f"Total Price: ${total}\n")
    return True