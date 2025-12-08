# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

from db.crud import fetch, insert, update, delete

def db_fetch_user_addresses(user_id):
    """查詢使用者的所有地址
    
    Args:
        user_id: 使用者 ID
    
    Returns:
        list: 地址列表
    """
    conditions = {"user_id": user_id}
    rows = fetch("USER_ADDRESS", conditions, order_by="address_id")
    
    # USER_ADDRESS 表欄位：address_id, user_id, district, label, address
    return [
        {
            "address_id": row[0],
            "user_id": row[1],
            "district": row[2],
            "label": row[3],
            "address": row[4],
        }
        for row in rows
    ]


def db_create_user_address(user_id, district, label, address):
    """新增使用者地址
    
    Args:
        user_id: 使用者 ID
        district: 行政區
        label: 地址標籤（例如：家、公司）
        address: 詳細地址
    
    Returns:
        int: 新增的地址 ID
    """
    address_data = {
        "user_id": user_id,
        "district": district,
        "label": label,
        "address": address,
    }
    
    address_id = insert("USER_ADDRESS", address_data)
    return address_id


def db_update_user_address(address_id, user_id, **updates):
    """更新使用者地址
    
    Args:
        address_id: 地址 ID
        user_id: 使用者 ID（用於驗證地址所有權）
        **updates: 要更新的欄位（district, label, address）
    
    Returns:
        tuple: 更新後的記錄
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證地址所有權
    conditions = {"address_id": address_id, "user_id": user_id}
    existing = fetch("USER_ADDRESS", conditions)
    
    if not existing:
        raise ValueError("地址不存在或不屬於您")
    
    row = update("USER_ADDRESS", updates, conditions)
    return row


def db_delete_user_address(address_id, user_id):
    """刪除使用者地址
    
    Args:
        address_id: 地址 ID
        user_id: 使用者 ID（用於驗證地址所有權）
    
    Returns:
        tuple: 刪除的記錄
    """
    # 驗證地址所有權
    conditions = {"address_id": address_id, "user_id": user_id}
    existing = fetch("USER_ADDRESS", conditions)
    
    if not existing:
        raise ValueError("地址不存在或不屬於您")
    
    row = delete("USER_ADDRESS", conditions)
    return row
