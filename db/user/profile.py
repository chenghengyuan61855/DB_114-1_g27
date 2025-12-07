from db.crud import fetch, update

def db_fetch_user_profile(user_id):
    """查詢用戶的個人資料"""
    users = fetch("APP_USER", {"user_id": user_id})
    if not users:
        return None
    
    row = users[0]
    profile = {
        "user_id": row[0],
        "user_name": row[1],
        "user_phone": row[2],
        "user_email": row[3],
        "password_hash": row[4],
        "is_active": row[5],
    }
    return profile

def db_update_user_profile(user_id, updates):
    """更新用戶的個人資料（姓名、email等）"""
    updated_rows = update("APP_USER", updates, {"user_id": user_id})
    return updated_rows