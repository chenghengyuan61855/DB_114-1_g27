from ui.helper import cancel_check
from db.order_rating.fetch import fetch_order_item_details

def rating_input(context:str):
    """檢查評分輸入是否有效或是否取消"""
    valid_rating = {'1', '2', '3', '4', '5'}
    while True:
        rating_input_str = input("Please enter a rating (1-5 stars): ").strip()
        if rating_input_str.lower() == ':q':
            return ":q"
        if rating_input_str not in valid_rating:
            print("Invalid rating. Please enter a number between 1 and 5.")
            continue
        return int(rating_input_str)
    
def show_order_item_details(order_item_id):
    """顯示訂單項目詳細資訊
    
    Args:
        order_item_id (int): 訂單項目ID

    Returns:
        bool: 是否成功顯示訂單項目詳細資訊
    """
    main, options, totals = fetch_order_item_details(order_item_id)
    
    if not main or not totals:
        print("❌ 找不到訂單項目")
        return False

    # main = (order_item_id, display_name, unit_price, qty)
    # totals = (option_total_adjust, line_total_price)
    
    print("\n訂單項目詳情：")
    print(f"品項：{main[1]}")  # display_name
    print(f"單價：${main[2]}")  # unit_price
    print(f"數量：{main[3]}")    # qty
    
    if options:
        print("客製化選項：")
        for option in options:
            option_name = option[0]
            price_adjust = option[1]
            price_str = f"+${price_adjust}" if price_adjust > 0 else "免費"
            print(f"  • {option_name} ({price_str})")
        print(f"選項加價：${totals[0]}")  # option_total_adjust
    else:
        print("客製化選項：無")
    
    print(f"小計：${totals[1]}\n")  # line_total_price
    return True