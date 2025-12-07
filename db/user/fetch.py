# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-07
# ============================

from db.crud import selective_fetch

def db_fetch_user_role(user_id):
    """查詢用戶的所有角色
    
    Args:
        user_id: 用戶 ID
    
    Returns:
        list: 角色名稱列表，例如 ['customer', 'store_manager']
    """
    # 查詢 USER_ROLE_ASSIGNMENT 表
    assignments = selective_fetch(
        "USER_ROLE_ASSIGNMENT",
        ["role_id"],
        {"user_id": user_id, "is_active": True}
    )
    
    if not assignments:
        return []
    
    # 取得所有 role_id
    role_ids = [row[0] for row in assignments]
    
    # 查詢對應的 role_name
    roles = []
    for role_id in role_ids:
        role_data = selective_fetch(
            "ROLE",
            ["role_name"],
            {"role_id": role_id, "is_active": True}
        )
        if role_data:
            roles.append(role_data[0][0])
    
    return roles