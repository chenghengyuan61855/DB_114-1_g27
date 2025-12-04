from db.common import fetch

def login_user(user_phone, password_hash):
    users = fetch("app_user", {"user_phone": user_phone, "password_hash": password_hash, "is_active": True})
    if not users:
        return None
    
    row = users[0]
    user_id = row[0]
    return user_id
