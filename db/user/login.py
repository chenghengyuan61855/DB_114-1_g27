from db.crud import fetch

def db_login_user(user_phone, password_hash):
    users = fetch("APP_USER", {"user_phone": user_phone, "password_hash": password_hash, "is_active": True})
    if not users:
        return None
    
    row = users[0]
    user_id = row[0]
    return user_id
