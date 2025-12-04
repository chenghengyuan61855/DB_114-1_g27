from app.db.db_common import insert, update, fetch, exists
from app.db.db_conn import commit

# ---------- User & Role ----------

def create_user(user_name, user_email, user_phone, password_hash):
    if exists("app_user", {"user_email": user_email}):
        raise ValueError("Email already registered")
    if exists("app_user", {"user_name": user_name}):
        raise ValueError("Username already taken")
    
    return insert("app_user", {
        "user_name": user_name,
        "user_email": user_email,
        "user_phone": user_phone,
        "password_hash": password_hash,
        "is_active": True,
    })

# ---------- Brand ----------

def create_brand(name, address=None, phone=None, email=None):
    if exists("brand", {"brand_name": name}):
        raise ValueError("Brand name already exists")

    return insert("brand", {
        "brand_name": name,
        "brand_address": address,
        "brand_phone": phone,
        "brand_email": email,
        "is_active": True,
    })

def update_brand(brand_id, data: dict):
    return update("brand", data, {"brand_id": brand_id})

# ---------- Store ----------

def create_store(brand_id, name, address=None, phone=None):
    return insert("store", {
        "brand_id": brand_id,
        "store_name": name,
        "store_address": address,
        "store_phone": phone,
        "is_active": True,
        "is_accepting_orders": True,
        "is_accepting_deliveries": True,
        "delivery_threshold_logic": "any",
    })

def update_store_basic(store_id, data: dict):
    """
    data 例如：
    {
      "store_phone": "...",
      "store_address": "...",
      "is_accepting_orders": False,
      "is_accepting_deliveries": True,
      "min_order_qty": 2,
      "min_order_total_price": 150,
      "delivery_threshold_logic": "all"
    }
    """
    return update("store", data, {"store_id": store_id})

# ---------- Store Hours ----------

def set_store_hours(store_id, weekday, is_open, open_time=None, close_time=None):
    """
    weekday: 0~6
    open_time / close_time: 'HH:MM' 字串或 datetime.time
    """
    # 如果該 store / weekday 已存在 → update
    if exists("store_hours", {"store_id": store_id, "weekday": weekday}):
        return update(
            "store_hours",
            {
                "is_open": is_open,
                "open_time": open_time,
                "close_time": close_time,
            },
            {
                "store_id": store_id,
                "weekday": weekday,
            },
        )
    else:
        return insert("store_hours", {
            "store_id": store_id,
            "weekday": weekday,
            "is_open": is_open,
            "open_time": open_time,
            "close_time": close_time,
        })

def get_store_hours(store_id):
    return fetch("store_hours", {"store_id": store_id})
