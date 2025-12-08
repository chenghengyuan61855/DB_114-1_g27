# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-08
# ASSISTED BY: Claude
# ============================

from db.crud import update

def db_update_store_product_status(store_id, product_id, is_active):
    """更新門市商品狀態
    
    此函式用於啟用或停用某個門市的特定商品，例如：
    - 某商品缺貨，可以暫時停用
    - 補貨後，重新啟用
    
    使用範例：
        # 停用某門市的「珍珠奶茶」
        db_update_store_product_status(store_id=2, product_id=11, is_active=False)
        
        # 重新啟用
        db_update_store_product_status(store_id=2, product_id=11, is_active=True)
    
    Args:
        store_id (int): 門市 ID
        product_id (int): 商品 ID
        is_enabled (bool): 是否啟用（True=啟用，False=停用）
    
    Returns:
        tuple: 更新後的完整記錄
    
    注意事項：
        - 此操作不會影響其他門市的同一商品
        - 停用後，該門市的顧客將無法購買此商品
    """
    row = update(
        "STORE_PRODUCT",
        {"is_active": is_active},
        {"store_id": store_id, "product_id": product_id}
    )
    return row