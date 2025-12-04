from app.db.db_common import insert, update, fetch, exists, delete
from app.db.db_conn import commit

def login_user(user_phone, password_hash):
    users = fetch("app_user", {"user_phone": user_phone, "password_hash": password_hash, "is_active": True})
    if not users:
        return None
    
    row = users[0]
    user_id = row[0]
    return user_id

def create_user(user_name, user_email, user_phone, password_hash):
    if exists("app_user", {"user_phone": user_phone}):
        raise ValueError("Phone already registered")
    if user_email and exists("app_user", {"user_email": user_email}):
        raise ValueError("Email already taken")
    
    row = insert("app_user", {
        "user_name": user_name,
        "user_email": user_email,
        "user_phone": user_phone,
        "password_hash": password_hash,
        "is_active": True,
    })
    
    return row[0]
