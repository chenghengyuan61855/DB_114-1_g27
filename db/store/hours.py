from db.crud import fetch, insert, update

def db_fetch_store_hours(store_id):
    """查詢門市營業時間
    
    Args:
        store_id: 門市 ID
    
    Returns:
        list: 營業時間列表（週日=0 到週六=6）
    """
    rows = fetch("STORE_HOURS", {"store_id": store_id}, order_by="weekday")
    
    return [
        {
            "store_id": row[0],
            "weekday": row[1],
            "is_open": row[2],
            "open_time": row[3],
            "close_time": row[4],
        }
        for row in rows
    ]


def db_create_store_hours(store_id, weekday, is_open, open_time=None, close_time=None):
    """新增門市營業時間
    
    Args:
        store_id: 門市 ID
        weekday: 星期幾（0=週日, 1=週一, ..., 6=週六）
        is_open: 是否營業
        open_time: 營業開始時間（格式：'HH:MM:SS'）
        close_time: 營業結束時間（格式：'HH:MM:SS'）
    
    Returns:
        tuple: 新增的記錄
    
    Raises:
        ValueError: 如果參數無效
    """
    if not (0 <= weekday <= 6):
        raise ValueError("Weekday must be between 0 (Sunday) and 6 (Saturday)")
    
    if is_open and (not open_time or not close_time):
        raise ValueError("Open time and close time are required when store is open")
    
    row = insert("STORE_HOURS", {
        "store_id": store_id,
        "weekday": weekday,
        "is_open": is_open,
        "open_time": open_time,
        "close_time": close_time,
    })
    
    return row


def db_update_store_hours(store_id, weekday, **updates):
    """更新門市營業時間
    
    Args:
        store_id: 門市 ID
        weekday: 星期幾（0-6）
        **updates: 要更新的欄位
            - is_open: 是否營業
            - open_time: 營業開始時間
            - close_time: 營業結束時間
    
    Returns:
        tuple: 更新後的記錄
    
    Raises:
        ValueError: 如果 updates 為空
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證欄位
    allowed_fields = {"is_open", "open_time", "close_time"}
    invalid_fields = set(updates.keys()) - allowed_fields
    
    if invalid_fields:
        raise ValueError(f"Invalid fields: {invalid_fields}")
    
    row = update("STORE_HOURS", updates, {"store_id": store_id, "weekday": weekday})
    return row


def db_init_store_hours(store_id):
    """初始化門市營業時間（預設全週營業 10:00-22:00）
    
    Args:
        store_id: 門市 ID
    
    Returns:
        int: 新增的記錄數量
    """
    weekday_names = ["週日", "週一", "週二", "週三", "週四", "週五", "週六"]
    count = 0
    
    for weekday in range(7):
        try:
            db_create_store_hours(
                store_id=store_id,
                weekday=weekday,
                is_open=True,
                open_time="10:00:00",
                close_time="22:00:00"
            )
            count += 1
        except Exception as e:
            print(f"❌ 初始化 {weekday_names[weekday]} 失敗: {e}")
    
    return count
