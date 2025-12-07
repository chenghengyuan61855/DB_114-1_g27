# db/inventory/manage.py
# ============================
# AUTHOR: KUO
# EDIT DATE: 2025-12-07
# ASSISTED BY: Claude
# ============================

from db.crud import insert, update, fetch
from datetime import datetime

def db_create_inventory(store_id, ingredient_id, stock_level):
    """建立原料庫存記錄
    
    Args:
        store_id: 門市 ID
        ingredient_id: 原料 ID
        stock_level: 庫存數量
    
    Returns:
        row: 完整的庫存記錄
    """
    if stock_level < 0:
        raise ValueError("Stock level cannot be negative")
    
    row = insert("INVENTORY", {
        "store_id": store_id,
        "ingredient_id": ingredient_id,
        "stock_level": stock_level,
        "last_restock_at": datetime.now(),
    })
    return row


def db_fetch_inventory(store_id=None, ingredient_id=None):
    """查詢庫存
    
    Args:
        store_id: 門市 ID
        ingredient_id: 原料 ID
    
    Returns:
        list: 庫存列表
    """
    conditions = {}
    if store_id:
        conditions["store_id"] = store_id
    if ingredient_id:
        conditions["ingredient_id"] = ingredient_id
    
    rows = fetch("INVENTORY", conditions if conditions else None)
    return [
        {
            "store_id": row[0],
            "ingredient_id": row[1],
            "stock_level": row[2],
            "last_restock_at": row[3],
        }
        for row in rows
    ]


def db_update_inventory(store_id, ingredient_id, new_stock_level):
    """更新庫存數量
    
    Args:
        store_id: 門市 ID
        ingredient_id: 原料 ID
        new_stock_level: 新庫存數量
    
    Returns:
        row: 更新後的記錄
    """
    if new_stock_level < 0:
        raise ValueError("Stock level cannot be negative")
    
    row = update("INVENTORY", 
                {"stock_level": new_stock_level, "updated_at": datetime.now()},
                {"store_id": store_id, "ingredient_id": ingredient_id})
    return row


def db_deduct_inventory(store_id, ingredient_id, qty):
    """扣減庫存（用於下單）
    
    Args:
        store_id: 門市 ID
        ingredient_id: 原料 ID
        qty: 扣減數量
    
    Returns:
        dict: 更新後的庫存資料
    
    Raises:
        ValueError: 庫存不足
    """
    inventory = fetch("INVENTORY", {"store_id": store_id, "ingredient_id": ingredient_id})
    if not inventory:
        raise ValueError(f"Inventory record not found for store {store_id}, ingredient {ingredient_id}")
    
    current_stock = inventory[0][2]
    if current_stock < qty:
        raise ValueError(f"Insufficient stock. Available: {current_stock}, Requested: {qty}")
    
    new_stock = current_stock - qty
    row = update("INVENTORY",
                {"stock_level": new_stock, "updated_at": datetime.now()},
                {"store_id": store_id, "ingredient_id": ingredient_id})
    
    return {
        "store_id": row[0],
        "ingredient_id": row[1],
        "stock_level": row[2],
    }