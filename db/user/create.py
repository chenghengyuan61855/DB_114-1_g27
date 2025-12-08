from db.crud import insert, exists
from db import conn  

def db_create_user(user_name, user_email, user_phone, password_hash):
    if exists("APP_USER", {"user_phone": user_phone}):
        raise ValueError("Phone already registered")
    if user_email and exists("APP_USER", {"user_email": user_email}):
        raise ValueError("Email already taken")
    
    row = insert("APP_USER", {
        "user_name": user_name,
        "user_email": user_email,
        "user_phone": user_phone,
        "password_hash": password_hash,
        "is_active": True,
    })
    
    conn.commit() 
    
    return row[0]
