from db.crud import fetch
import bcrypt  # ← 新增

def db_login_user(user_phone, password):
    """使用者登入（使用 bcrypt 驗證）"""
    
    # 1. 查詢使用者
    users = fetch("APP_USER", {
        "user_phone": user_phone,
        "is_active": True
    })
    
    if not users:
        return None
    
    row = users[0]
    user_id = row[0]
    stored_hash = row[4]  # password_hash 欄位
    
    # 2. 驗證密碼
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return user_id
    else:
        return None