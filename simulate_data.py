import random
from datetime import datetime, timedelta
import bcrypt

# ============================================
# 配置參數
# ============================================
NUM_USERS = 5000  # 生成 5000 個會員
NUM_ORDERS = 50000  # 生成 50000 筆訂單

# 門市 ID 範圍（根據你的 reset_database.sql）
STORE_IDS = list(range(1, 10))  # 1-9

# 商品 ID 範圍（根據你的資料）
PRODUCT_IDS = list(range(1, 51))  # 1-50

# 選項分類與選項對應（簡化版）
OPTION_CATEGORIES = {
    1: [1, 2, 3, 4],      # 可不可 - 甜度
    2: [5, 6, 7, 8],      # 可不可 - 冰塊
    3: [9, 10, 11],       # 可不可 - 配料
    4: [12, 13, 14, 15],  # 50嵐 - 甜度
    5: [16, 17, 18, 19],  # 50嵐 - 冰塊
    6: [20, 21, 22],      # 50嵐 - 配料
}

# ============================================
# 生成會員資料
# ============================================
def generate_users(num_users, start_id=10):
    """生成會員資料"""
    print("-- =============================================")
    print(f"-- 生成 {num_users} 個會員")
    print("-- =============================================")
    
    # 預設密碼 hash（密碼：test123）
    # 使用 bcrypt 生成，所有測試帳號密碼都是 test123
    default_password = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    sql_values = []
    for i in range(start_id, start_id + num_users):
        user_name = f"user_{i:06d}"
        user_phone = f"09{random.randint(10000000, 99999999)}"
        user_email = f"user{i}@example.com"
        
        sql_values.append(
            f"({i}, '{user_name}', '{user_phone}', '{user_email}', '{default_password}', true)"
        )
    
    print("INSERT INTO APP_USER (user_id, user_name, user_phone, user_email, password_hash, is_active) VALUES")
    
    # 每 1000 筆分批輸出
    batch_size = 1000
    for i in range(0, len(sql_values), batch_size):
        batch = sql_values[i:i+batch_size]
        print(",\n".join(batch) + ";")
        if i + batch_size < len(sql_values):
            print("\nINSERT INTO APP_USER (user_id, user_name, user_phone, user_email, password_hash, is_active) VALUES")
    
    print()

# ============================================
# 生成會員角色分配
# ============================================
def generate_user_roles(num_users, start_id=10):
    """為所有會員分配 member 角色"""
    print("-- =============================================")
    print(f"-- 為 {num_users} 個會員分配角色")
    print("-- =============================================")
    
    sql_values = []
    for i in range(start_id, start_id + num_users):
        sql_values.append(f"({i}, 1, 'global', NULL, NULL)")
    
    print("INSERT INTO USER_ROLE_ASSIGNMENT (user_id, role_id, scope_type, brand_id, store_id) VALUES")
    
    batch_size = 1000
    for i in range(0, len(sql_values), batch_size):
        batch = sql_values[i:i+batch_size]
        print(",\n".join(batch) + ";")
        if i + batch_size < len(sql_values):
            print("\nINSERT INTO USER_ROLE_ASSIGNMENT (user_id, role_id, scope_type, brand_id, store_id) VALUES")
    
    print()

# ============================================
# 生成訂單資料
# ============================================
def generate_orders(num_orders, user_start_id=20, user_end_id=5000):
    """生成訂單資料"""
    print("-- =============================================")
    print(f"-- 生成 {num_orders} 筆訂單")
    print("-- =============================================")
    
    order_statuses = ['placed', 'accepted', 'completed', 'rejected', 'cancelled']
    order_status_weights = [0.1, 0.15, 0.65, 0.05, 0.05]  # 大部分是已完成
    
    order_types = ['pickup', 'delivery']
    payment_methods = ['cash', 'card', 'online']  # ✅ 修正：符合 VARCHAR(10) 限制
    payment_statuses = ['paid', 'unpaid']
    
    districts = ['大安區', '中正區', '信義區', '松山區', '萬華區', '中山區']
    
    # 生成過去 90 天的訂單
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    sql_values = []
    
    for i in range(num_orders):
        user_id = random.randint(user_start_id, user_end_id)
        store_id = random.choice(STORE_IDS)
        order_status = random.choices(order_statuses, weights=order_status_weights)[0]
        order_type = random.choice(order_types)
        payment_method = random.choice(payment_methods)
        payment_status = 'paid' if order_status in ['completed', 'accepted'] else random.choice(payment_statuses)
        
        # 隨機生成時間
        placed_at = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        placed_at_str = placed_at.strftime('%Y-%m-%d %H:%M:%S')
        
        # 外送相關資訊
        if order_type == 'delivery':
            district = random.choice(districts)
            delivery_address = f"台北市{district}測試路{random.randint(1, 500)}號"
            receiver_name = f"收件人_{random.randint(1000, 9999)}"
            receiver_phone = f"09{random.randint(10000000, 99999999)}"
            delivery_sql = f"'{delivery_address}', '{receiver_name}', '{receiver_phone}'"
        else:
            delivery_sql = "NULL, NULL, NULL"
        
        # 計算訂單總價（先預設，之後會根據訂單項目更新）
        total_price = random.randint(50, 500)
        
        # 時間戳記
        accepted_at = "NULL"
        completed_at = "NULL"
        rejected_reason = "NULL"
        
        if order_status == 'accepted':
            accepted_at = f"'{(placed_at + timedelta(minutes=random.randint(1, 10))).strftime('%Y-%m-%d %H:%M:%S')}'"
        elif order_status == 'completed':
            accepted_at = f"'{(placed_at + timedelta(minutes=random.randint(1, 10))).strftime('%Y-%m-%d %H:%M:%S')}'"
            completed_at = f"'{(placed_at + timedelta(minutes=random.randint(15, 60))).strftime('%Y-%m-%d %H:%M:%S')}'"
        elif order_status == 'rejected':
            rejected_reason = "'門市忙碌中'"
        
        sql_values.append(
            f"({user_id}, {store_id}, '{order_status}', '{order_type}', "
            f"{delivery_sql}, '{placed_at_str}', {accepted_at}, {completed_at}, "
            f"{rejected_reason}, {total_price}, '{payment_status}', '{payment_method}')"
        )
    
    print("INSERT INTO ORDERS (user_id, store_id, order_status, order_type, "
          "delivery_address, receiver_name, receiver_phone, placed_at, accepted_at, "
          "completed_at, rejected_reason, total_price, payment_status, payment_method) VALUES")
    
    batch_size = 1000
    for i in range(0, len(sql_values), batch_size):
        batch = sql_values[i:i+batch_size]
        print(",\n".join(batch) + ";")
        if i + batch_size < len(sql_values):
            print("\nINSERT INTO ORDERS (user_id, store_id, order_status, order_type, "
                  "delivery_address, receiver_name, receiver_phone, placed_at, accepted_at, "
                  "completed_at, rejected_reason, total_price, payment_status, payment_method) VALUES")
    
    print()

# ============================================
# 生成訂單項目資料
# ============================================
def generate_order_items(num_orders, order_start_id=1):
    """生成訂單項目資料"""
    print("-- =============================================")
    print(f"-- 生成訂單項目（每筆訂單 1-5 個商品）")
    print("-- =============================================")
    
    sql_values = []
    order_item_id = 1
    
    for order_id in range(order_start_id, order_start_id + num_orders):
        # 每筆訂單隨機 1-5 個商品
        num_items = random.randint(1, 5)
        
        for _ in range(num_items):
            product_id = random.choice(PRODUCT_IDS)
            unit_price = random.randint(30, 80)
            qty = random.randint(1, 3)
            option_total_adjust = random.randint(0, 30)
            line_total_price = (unit_price + option_total_adjust) * qty
            
            sql_values.append(
                f"({order_item_id}, {order_id}, {product_id}, {unit_price}, {qty}, "
                f"{option_total_adjust}, {line_total_price})"
            )
            order_item_id += 1
    
    print("INSERT INTO ORDER_ITEM (order_item_id, order_id, product_id, unit_price, qty, "
          "option_total_adjust, line_total_price) VALUES")
    
    batch_size = 1000
    for i in range(0, len(sql_values), batch_size):
        batch = sql_values[i:i+batch_size]
        print(",\n".join(batch) + ";")
        if i + batch_size < len(sql_values):
            print("\nINSERT INTO ORDER_ITEM (order_item_id, order_id, product_id, unit_price, qty, "
                  "option_total_adjust, line_total_price) VALUES")
    
    print()

# ============================================
# 生成訂單項目選項資料
# ============================================
def generate_order_item_options(num_order_items_approx):
    """為每個訂單項目添加客製化選項"""
    print("-- =============================================")
    print(f"-- 生成訂單項目選項（每個商品約 2-4 個選項）")
    print("-- =============================================")
    
    sql_values = []
    
    for order_item_id in range(1, num_order_items_approx + 1):
        # 隨機選擇 2-4 個選項
        num_options = random.randint(2, 4)
        selected_options = random.sample(range(1, 23), num_options)
        
        for option_id in selected_options:
            sql_values.append(f"({order_item_id}, {option_id})")
    
    print("INSERT INTO ORDER_ITEM_OPTION (order_item_id, option_id) VALUES")
    
    batch_size = 1000
    for i in range(0, len(sql_values), batch_size):
        batch = sql_values[i:i+batch_size]
        print(",\n".join(batch) + ";")
        if i + batch_size < len(sql_values):
            print("\nINSERT INTO ORDER_ITEM_OPTION (order_item_id, option_id) VALUES")
    
    print()

# ============================================
# 主程式
# ============================================
if __name__ == "__main__":
    print("-- =============================================")
    print("-- daTEAbase 測試資料生成器")
    print(f"-- 生成日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-- =============================================\n")
    
    # 1. 生成會員
    generate_users(NUM_USERS)
    
    # 2. 分配角色
    generate_user_roles(NUM_USERS)
    
    # 3. 生成訂單
    generate_orders(NUM_ORDERS)
    
    # 4. 生成訂單項目（估計約 2.5 個商品/訂單）
    generate_order_items(NUM_ORDERS)
    
    # 5. 生成訂單項目選項（估計約 2.5 * 3 = 7.5 個選項/訂單）
    estimated_order_items = NUM_ORDERS * 3
    generate_order_item_options(estimated_order_items)
    
    print("\n-- =============================================")
    print("-- 生成完成！")
    print("-- =============================================")