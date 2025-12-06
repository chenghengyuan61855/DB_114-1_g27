from db.crud import fetch, update

def db_view_user_profile(user_id):
    users = fetch("APP_USER", {"user_id": user_id})
    if not users:
        return None
    
    row = users[0]
    profile = {
        "user_id": row[0],
        "user_name": row[1],
        "user_phone": row[2],
        "user_email": row[3],
        "is_active": row[5],
    }
    return profile

def db_update_user_profile(user_id, updates):
    updated_rows = update("APP_USER", updates, {"user_id": user_id})
    return updated_rows