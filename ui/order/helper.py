def go_back_check(input_str):
    """
    Checks if the user input indicates going back to the previous step.
    Returns True if the input is ':b', False otherwise.
    """
    return input_str.strip() == ":b"

def go_back(step):
    """
    Determines the previous step based on the current step.
    Returns the previous step number or None if at the first step.
    """
    if step > 0:
        return step - 1
    return 0

def is_accepting_orders_check(store_id):
    """
    Checks if the store is currently accepting orders.
    Returns True if accepting, False otherwise.
    """
    from db.store.fetch import db_fetch_is_accepting_orders
    accepting = db_fetch_is_accepting_orders(store_id)
    if not accepting:
        print("❌ Store is not accepting orders at the moment.")
        return False
    return True