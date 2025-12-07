# ============================
# AUTHOR: KUO
# CREATED DATE: 2025-12-07
# LAST EDIT: 2025-12-07
# ASSISTED BY: Claude
# ============================
# 
# 此檔案負責選項相關的「更新」與「刪除」操作
# 
# 功能概覽：
# 1. 更新選項分類（如：修改「甜度」的顯示順序）
# 2. 更新選項（如：修改「珍珠」的價格調整）
# 3. 更新商品選項規則（如：修改某商品的甜度必選數量）
# 4. 更新門市選項狀態（如：某門市停用「珍珠」選項）
# 5. 刪除選項分類（軟刪除：設定 is_active = False）
# 6. 刪除選項（軟刪除：設定 is_active = False）
# 7. 刪除商品選項規則（硬刪除：從資料庫移除記錄）
# 8. 刪除互斥規則（硬刪除：從資料庫移除記錄）
# 9. 刪除門市選項設定（硬刪除：從資料庫移除記錄）
# 
# 軟刪除 vs 硬刪除：
# - 軟刪除：保留記錄但設定 is_active = False（用於有歷史記錄需求的資料）
# - 硬刪除：直接從資料庫刪除記錄（用於純配置型資料）
# ============================

from db.crud import update, delete

# ==================== UPDATE 函式 ====================

def db_update_option_category(o_category_id, **updates):
    """更新選項分類
    
    此函式用於修改選項分類的資訊，例如：
    - 修改分類名稱（如：「甜度」改為「糖度」）
    - 修改顯示順序（如：將「甜度」從第 3 位調整到第 1 位）
    - 啟用/停用分類（設定 is_active）
    
    使用範例：
        # 修改分類名稱
        db_update_option_category(1, o_category_name="糖度")
        
        # 修改顯示順序
        db_update_option_category(1, display_order=1)
        
        # 停用分類
        db_update_option_category(1, is_active=False)
        
        # 同時修改多個欄位
        db_update_option_category(1, o_category_name="糖度", display_order=1)
    
    Args:
        o_category_id (int): 選項分類 ID（必填，用於定位要更新的記錄）
        **updates (dict): 要更新的欄位及其新值，可包含：
            - o_category_name (str): 新的分類名稱
            - display_order (int): 新的顯示順序
            - is_active (bool): 是否啟用
    
    Returns:
        tuple: 更新後的完整記錄（由 db.crud.update() 返回）
    
    Raises:
        ValueError: 如果 updates 為空（沒有要更新的欄位）
        psycopg2.Error: 如果資料庫操作失敗（如：ID 不存在）
    
    注意事項：
        - 必須至少提供一個要更新的欄位，否則會拋出 ValueError
        - 此函式不驗證欄位值的合法性，應在 UI 層先驗證
    """
    if not updates:
        raise ValueError("No fields to update")
    
    row = update("OPTION_CATEGORY", updates, {"o_category_id": o_category_id})
    return row


def db_update_option(option_id, **updates):
    """更新選項
    
    此函式用於修改選項的資訊，例如：
    - 修改選項名稱（如：「珍珠」改為「黑糖珍珠」）
    - 修改價格調整（如：珍珠從 +10 改為 +15）
    - 啟用/停用選項
    
    使用範例：
        # 修改選項名稱
        db_update_option(5, option_name="黑糖珍珠")
        
        # 修改價格調整
        db_update_option(5, price_adjust=15)
        
        # 停用選項
        db_update_option(5, is_active=False)
    
    Args:
        option_id (int): 選項 ID（必填，用於定位要更新的記錄）
        **updates (dict): 要更新的欄位及其新值，可包含：
            - option_name (str): 新的選項名稱
            - price_adjust (int): 新的價格調整（-1000 到 1000）
            - is_active (bool): 是否啟用
    
    Returns:
        tuple: 更新後的完整記錄
    
    Raises:
        ValueError: 
            - 如果 updates 為空
            - 如果 price_adjust 超出範圍（-1000 到 1000）
    
    注意事項：
        - price_adjust 必須在 -1000 到 1000 之間
        - 負值表示優惠（如：-5 表示便宜 5 元）
        - 正值表示加價（如：+10 表示多收 10 元）
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證 price_adjust 的範圍
    if "price_adjust" in updates:
        if updates["price_adjust"] < -1000 or updates["price_adjust"] > 1000:
            raise ValueError("Price adjustment must be between -1000 and 1000")
    
    row = update("OPTION", updates, {"option_id": option_id})
    return row


def db_update_brand_product_option_rule(brand_id, product_id, o_category_id, **updates):
    """更新商品選項規則
    
    此函式用於修改商品的選項規則，例如：
    - 修改某商品的甜度必選數量（min_select, max_select）
    - 修改預設選項（default_option_id）
    
    使用範例：
        # 將某商品的甜度從「必選 1 個」改為「最多選 2 個」
        db_update_brand_product_option_rule(
            brand_id=1, 
            product_id=10, 
            o_category_id=2,  # 假設 2 是「甜度」分類
            min_select=0,
            max_select=2
        )
        
        # 修改預設選項
        db_update_brand_product_option_rule(
            brand_id=1, 
            product_id=10, 
            o_category_id=2,
            default_option_id=15  # 假設 15 是「半糖」選項
        )
    
    Args:
        brand_id (int): 品牌 ID（必填，用於定位規則）
        product_id (int): 商品 ID（必填，用於定位規則）
        o_category_id (int): 選項分類 ID（必填，用於定位規則）
        **updates (dict): 要更新的欄位及其新值，可包含：
            - min_select (int): 最少要選幾個（0 表示可選可不選）
            - max_select (int): 最多可選幾個
            - default_option_id (int): 預設選項 ID
    
    Returns:
        tuple: 更新後的完整記錄
    
    Raises:
        ValueError:
            - 如果 updates 為空
            - 如果 min_select 或 max_select 為負數
            - 如果 min_select > max_select
    
    注意事項：
        - 規則由 (brand_id, product_id, o_category_id) 三個欄位唯一定位
        - min_select 和 max_select 必須同時滿足：
          * 非負數
          * min_select <= max_select
        - 例如：min_select=1, max_select=1 表示「必選 1 個」
        - 例如：min_select=0, max_select=3 表示「最多選 3 個，可不選」
    """
    if not updates:
        raise ValueError("No fields to update")
    
    # 驗證選擇範圍的合法性
    if "min_select" in updates or "max_select" in updates:
        # 取得更新後的值（如果沒有更新則使用預設值 0）
        min_select = updates.get("min_select", 0)
        max_select = updates.get("max_select", 0)
        
        # 檢查是否為負數
        if min_select < 0 or max_select < 0:
            raise ValueError("Min and max select cannot be negative")
        
        # 檢查邏輯一致性
        if min_select > max_select:
            raise ValueError("Min select cannot be greater than max select")
    
    # 定位條件：需要三個欄位才能唯一定位一條規則
    conditions = {
        "brand_id": brand_id,
        "product_id": product_id,
        "o_category_id": o_category_id
    }
    
    row = update("BRAND_PRODUCT_OPTION_RULE", updates, conditions)
    return row


def db_update_store_option(store_id, option_id, is_enabled):
    """更新門市選項狀態
    
    此函式用於啟用或停用某個門市的特定選項，例如：
    - 某門市的「珍珠」缺貨，可以暫時停用
    - 某門市進貨後，重新啟用「珍珠」
    
    使用範例：
        # 停用某門市的「珍珠」選項
        db_update_store_option(store_id=5, option_id=10, is_enabled=False)
        
        # 重新啟用
        db_update_store_option(store_id=5, option_id=10, is_enabled=True)
    
    Args:
        store_id (int): 門市 ID（必填）
        option_id (int): 選項 ID（必填）
        is_enabled (bool): 是否啟用（True=啟用，False=停用）
    
    Returns:
        tuple: 更新後的完整記錄
    
    注意事項：
        - 此操作不會影響其他門市的同一選項
        - 停用後，該門市的顧客將無法選擇此選項
        - 記錄會保留，方便日後重新啟用
    """
    row = update("STORE_OPTION", {"is_enabled": is_enabled}, {"store_id": store_id, "option_id": option_id})
    return row


# ==================== DELETE 函式 ====================

def db_delete_option_category(o_category_id):
    """刪除選項分類（軟刪除）
    
    此函式不會真正刪除資料，而是將 is_active 設為 False。
    
    為什麼使用軟刪除？
    - 保留歷史記錄（例如：過去的訂單曾經使用此分類）
    - 可以隨時恢復（只需將 is_active 改回 True）
    - 避免外鍵約束問題（其他表可能引用此分類）
    
    使用範例：
        # 停用「甜度」分類
        db_delete_option_category(2)
    
    Args:
        o_category_id (int): 選項分類 ID
    
    Returns:
        tuple: 更新後的記錄
    
    注意事項：
        - 軟刪除後，該分類下的所有選項仍存在
        - UI 層應該過濾掉 is_active=False 的記錄
        - 如果需要真正刪除，可使用 delete() 函式，但需注意外鍵約束
    """
    row = update("OPTION_CATEGORY", {"is_active": False}, {"o_category_id": o_category_id})
    return row


def db_delete_option(option_id):
    """刪除選項（軟刪除）
    
    此函式不會真正刪除資料，而是將 is_active 設為 False。
    
    使用範例：
        # 停用「珍珠」選項
        db_delete_option(10)
    
    Args:
        option_id (int): 選項 ID
    
    Returns:
        tuple: 更新後的記錄
    
    注意事項：
        - 軟刪除後，所有門市都無法使用此選項
        - 過去的訂單記錄仍會保留此選項的資訊
    """
    row = update("OPTION", {"is_active": False}, {"option_id": option_id})
    return row


def db_delete_brand_product_option_rule(brand_id, product_id, o_category_id):
    """刪除商品選項規則（硬刪除）
    
    此函式會真正從資料庫刪除規則記錄。
    
    為什麼使用硬刪除？
    - 選項規則是純配置資料，不涉及歷史記錄
    - 刪除後可以重新建立
    - 不需要保留已停用的規則
    
    使用範例：
        # 刪除某商品的「甜度」規則
        db_delete_brand_product_option_rule(
            brand_id=1,
            product_id=10,
            o_category_id=2
        )
    
    Args:
        brand_id (int): 品牌 ID
        product_id (int): 商品 ID
        o_category_id (int): 選項分類 ID
    
    Returns:
        int: 受影響的行數（通常為 1，如果為 0 表示記錄不存在）
    
    注意事項：
        - 刪除後無法恢復，除非重新建立
        - 刪除前應確認該商品不再需要此選項規則
    """
    conditions = {
        "brand_id": brand_id,
        "product_id": product_id,
        "o_category_id": o_category_id
    }
    
    row = delete("BRAND_PRODUCT_OPTION_RULE", conditions)
    return row


def db_delete_brand_product_option_mutex(mutex_id):
    """刪除互斥選項規則（硬刪除）
    
    此函式會真正從資料庫刪除互斥規則記錄。
    
    互斥規則範例：
    - 「冰」和「熱」不能同時選（EXCLUDE）
    - 「無糖」和「全糖」不能同時選（EXCLUDE）
    
    使用範例：
        # 刪除某個互斥規則
        db_delete_brand_product_option_mutex(mutex_id=5)
    
    Args:
        mutex_id (int): 互斥規則 ID
    
    Returns:
        int: 受影響的行數
    
    注意事項：
        - 刪除後，原本互斥的選項將可以同時選擇
        - 適用於需求變更的情況（如：某商品允許「冰」和「熱」混搭）
    """
    row = delete("BRAND_PRODUCT_OPTION_MUTEX", {"mutex_id": mutex_id})
    return row


def db_delete_store_option(store_id, option_id):
    """刪除門市選項設定（硬刪除）
    
    此函式會真正從資料庫刪除門市選項設定記錄。
    
    使用範例：
        # 移除某門市的「珍珠」選項設定
        db_delete_store_option(store_id=5, option_id=10)
    
    Args:
        store_id (int): 門市 ID
        option_id (int): 選項 ID
    
    Returns:
        int: 受影響的行數
    
    注意事項：
        - 刪除後，該門市將無法使用此選項
        - 如果需要重新啟用，必須重新建立記錄
        - 建議使用 db_update_store_option() 來停用，而非直接刪除
    """
    row = delete("STORE_OPTION", {"store_id": store_id, "option_id": option_id})
    return row


# ==================== 使用範例總結 ====================
"""
1. 更新選項分類名稱：
   db_update_option_category(1, o_category_name="糖度")

2. 更新選項價格：
   db_update_option(5, price_adjust=15)

3. 更新商品選項規則：
   db_update_brand_product_option_rule(1, 10, 2, min_select=0, max_select=2)

4. 停用門市選項：
   db_update_store_option(5, 10, is_enabled=False)

5. 軟刪除選項分類：
   db_delete_option_category(2)

6. 軟刪除選項：
   db_delete_option(10)

7. 硬刪除選項規則：
   db_delete_brand_product_option_rule(1, 10, 2)

8. 硬刪除互斥規則：
   db_delete_brand_product_option_mutex(5)

9. 硬刪除門市選項設定：
   db_delete_store_option(5, 10)
"""