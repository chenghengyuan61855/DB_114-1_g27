from db.common import insert, exists

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
