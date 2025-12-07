from ui.order.select_type import ui_select_order_type  # ← 修正檔名
from ui.order.select_brand import ui_select_brand
from ui.order.select_store import ui_select_store
from ui.order.select_items import ui_select_items
from ui.order.confirm_order import ui_confirm_and_submit_order
from ui.helper import clear_screen  # ← 新增 clear_screen

def ui_place_order(user_id):
    clear_screen()  # ← 開始點餐前清屏
    print("\n=== Place Order ===")
    print("(Type ':q' in any input to cancel order placement)")
    print("(Type ':b' in any input to go back to last step)\n")

    step = 0
    order_type = None
    brand_id = None
    store_id = None

    while True:
        if step == 0:
            order_type = ui_select_order_type()
            if order_type is None: return
            if order_type == ":b": continue
            step += 1

        if step == 1:
            brand_id = ui_select_brand()
            if brand_id is None: return
            if brand_id == ":b":
                step -= 1
                continue
            step += 1

        if step == 2:
            store_id = ui_select_store(order_type, brand_id)
            if store_id is None: return
            if store_id == ":b":
                step -= 1
                continue
            step += 1

        if step == 3:
            order_item = ui_select_items(brand_id, store_id)
            if order_item is None: return
            if order_item == ":b":
                step -= 1
                continue
            step += 1

        if step == 4:
            ui_confirm_and_submit_order(user_id, store_id, order_type, order_item)
            return