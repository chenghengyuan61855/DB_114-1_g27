from db.crud import fetch, insert, update, delete

def db_fetch_brand_stores(brand_id):
    """查詢品牌下的所有門市
    
    Args:
        brand_id: 品牌 ID
    
    Returns:
        list: 門市列表
    """
    rows = fetch("STORE", {"brand_id": brand_id}, order_by="store_id")
    
    return [
        {
            "store_id": row[0],
            "brand_id": row[1],
            "store_name": row[2],
            "store_address": row[3],
            "store_phone": row[4],
            "is_active": row[5],
            "is_accepting_orders": row[6],
            "created_at": row[7],
            "updated_at": row[8],
            "is_accepting_deliveries": row[9],
            "min_order_qty": row[10],
            "min_order_total_price": row[11],
            "delivery_threshold_logic": row[12],
        }
        for row in rows
    ]


def db_fetch_store_info(store_id):
    """查詢門市資訊
    
    Args:
        store_id: 門市 ID
    
    Returns:
        dict: 門市資訊
    """
    rows = fetch("STORE", {"store_id": store_id})
    
    if not rows:
        return None
    
    row = rows[0]
    return {
        "store_id": row[0],
        "brand_id": row[1],
        "store_name": row[2],
        "store_address": row[3],
        "store_phone": row[4],
        "is_active": row[5],
        "is_accepting_orders": row[6],
        "created_at": row[7],
        "updated_at": row[8],
        "is_accepting_deliveries": row[9],
        "min_order_qty": row[10],
        "min_order_total_price": row[11],
        "delivery_threshold_logic": row[12],
    }


def db_create_store(brand_id, store_name, store_address=None, store_phone=None):
    """新增門市
    
    Args:
        brand_id: 品牌 ID
        store_name: 門市名稱
        store_address: 門市地址（可選）
        store_phone: 門市電話（可選）
    
    Returns:
        int: 新門市的 ID
    
    Raises:
        ValueError: 如果門市名稱無效
    """
    if not store_name or len(store_name) > 20:
        raise ValueError("Store name must be 1-20 characters")
    
    row = insert("STORE", {
        "brand_id": brand_id,
        "store_name": store_name,
        "store_address": store_address,
        "store_phone": store_phone,
        "is_active": True,
        "is_accepting_orders": True,
        "is_accepting_deliveries": False,  # 預設不接受外送
    })
    
    return row[0]  # store_id


def db_update_store_info(store_id, **updates):
    """更新門市資訊
    
    Args:
        store_id: 門市 ID
        **updates: 要更新的欄位
            - store_name: 門市名稱
            - store_address: 門市地址
            - store_phone: 門市電話
            - is_active: 是否啟用
            - is_accepting_orders: 是否接受訂單
            - is_accepting_deliveries: 是否接受外送
            - min_order_qty: 最低訂購數量
            - min_order_total_price: 最低訂購金額
    
    Returns:
        tuple: 更新後的記錄
    
    Raises:
        ValueError: 如果 updates 為空或欄位無效
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證欄位
    allowed_fields = {
        "store_name", "store_address", "store_phone",
        "is_active", "is_accepting_orders", "is_accepting_deliveries",
        "min_order_qty", "min_order_total_price", "delivery_threshold_logic"
    }
    invalid_fields = set(updates.keys()) - allowed_fields
    
    if invalid_fields:
        raise ValueError(f"Invalid fields: {invalid_fields}")
    
    # 驗證門市名稱長度
    if "store_name" in updates and len(updates["store_name"]) > 20:
        raise ValueError("Store name must be 1-20 characters")
    
    row = update("STORE", updates, {"store_id": store_id})
    return row


def db_delete_store(store_id):
    """刪除門市（軟刪除 + 停用關聯資料）
    
    Args:
        store_id: 門市 ID
    
    Returns:
        tuple: 更新後的記錄
    
    Note:
        此操作會：
        1. 將門市設為停業狀態（is_active = False）
        2. 停止接單（is_accepting_orders = False）
        3. 停用該門市的所有商品（STORE_PRODUCT.is_active = False）
        4. 停用該門市的所有選項（STORE_OPTION.is_enabled = False）
        資料不會被刪除，但門市將不再接受訂單
    """
    from db import conn
    
    # 1. 軟刪除門市（設為停業且停止接單）
    row = update("STORE", {
        "is_active": False,
        "is_accepting_orders": False
    }, {"store_id": store_id})
    
    # 2. 停用該門市的所有商品
    conn.cur.execute(
        "UPDATE STORE_PRODUCT SET is_active = false WHERE store_id = %s",
        (store_id,)
    )
    
    # 3. 停用該門市的所有選項
    conn.cur.execute(
        "UPDATE STORE_OPTION SET is_enabled = false WHERE store_id = %s",
        (store_id,)
    )
    
    conn.commit()
    return row
