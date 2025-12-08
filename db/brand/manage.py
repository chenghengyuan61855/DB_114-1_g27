from db.crud import fetch, update

def db_fetch_brand_info(brand_id):
    """查詢品牌資訊
    
    Args:
        brand_id: 品牌 ID
    
    Returns:
        dict: 品牌資訊
    """
    rows = fetch("BRAND", {"brand_id": brand_id})
    
    if not rows:
        return None
    
    row = rows[0]
    return {
        "brand_id": row[0],
        "brand_name": row[1],
        "brand_address": row[2],
        "brand_phone": row[3],
        "brand_email": row[4],
        "is_active": row[5],
        "created_at": row[6],
        "updated_at": row[7],
    }


def db_update_brand_info(brand_id, **updates):
    """更新品牌資訊
    
    Args:
        brand_id: 品牌 ID
        **updates: 要更新的欄位
            - brand_name: 品牌名稱
            - brand_address: 品牌地址
            - brand_phone: 品牌電話
            - brand_email: 品牌 Email
            - is_active: 是否啟用
    
    Returns:
        tuple: 更新後的記錄
    
    Raises:
        ValueError: 如果 updates 為空
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證欄位
    allowed_fields = {"brand_name", "brand_address", "brand_phone", "brand_email", "is_active"}
    invalid_fields = set(updates.keys()) - allowed_fields
    
    if invalid_fields:
        raise ValueError(f"Invalid fields: {invalid_fields}")
    
    row = update("BRAND", updates, {"brand_id": brand_id})
    return row
