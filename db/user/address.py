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
    rows = fetch("USER_ADDRESS", conditions, order_by="label")
    
    # USER_ADDRESS 表欄位：user_id, label, district, address, created_at, updated_at
    return [
        {
            "user_id": row[0],
            "label": row[1],
            "district": row[2],
            "address": row[3],
            "created_at": row[4],
            "updated_at": row[5],
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
        bool: 是否成功新增
    """
    address_data = {
        "user_id": user_id,
        "district": district,
        "label": label,
        "address": address,
    }
    
    result = insert("USER_ADDRESS", address_data)
    return result is not None


def db_update_user_address(user_id, label, **updates):
    """更新使用者地址
    
    Args:
        user_id: 使用者 ID
        label: 地址標籤（用於識別要更新的地址）
        **updates: 要更新的欄位（district, address, 或 new_label）
    
    Returns:
        tuple: 更新後的記錄
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證地址存在
    conditions = {"user_id": user_id, "label": label}
    existing = fetch("USER_ADDRESS", conditions)
    
    if not existing:
        raise ValueError("地址不存在或不屬於您")
    
    # 如果要更新 label，需要特殊處理（因為 label 是主鍵的一部分）
    if "new_label" in updates:
        new_label = updates.pop("new_label")
        # 先刪除舊記錄
        delete("USER_ADDRESS", conditions)
        # 再新增新記錄
        new_data = {
            "user_id": user_id,
            "label": new_label,
            "district": existing[0][2] if "district" not in updates else updates["district"],
            "address": existing[0][3] if "address" not in updates else updates["address"],
        }
        insert("USER_ADDRESS", new_data)
        return fetch("USER_ADDRESS", {"user_id": user_id, "label": new_label})[0]
    
    row = update("USER_ADDRESS", updates, conditions)
    return row


def db_delete_user_address(user_id, label):
    """刪除使用者地址
    
    Args:
        user_id: 使用者 ID
        label: 地址標籤（用於識別要刪除的地址）
    
    Returns:
        tuple: 刪除的記錄
    """
    # 驗證地址存在
    conditions = {"user_id": user_id, "label": label}
    existing = fetch("USER_ADDRESS", conditions)
    
    if not existing:
        raise ValueError("地址不存在或不屬於您")
    
    row = delete("USER_ADDRESS", conditions)
    return row
