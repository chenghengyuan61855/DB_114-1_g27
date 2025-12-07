import psycopg2
import db.conn as conn
from db.allowed import table_check, column_check, data_check, conditions_check

def join_conditions(sql: str, table, conditions=None):
    params = []
    if conditions:
        clauses = []
        for key, value in conditions.items():
            column_check(table, key)
            clauses.append(f"{key} = %s")
            params.append(value)
        sql += " WHERE " + " AND ".join(clauses)
    return sql, params


def insert(table, data):
    table_check(table)
    data_check("Insert", data)

    columns = []
    values = []
    placeholders = []

    for key, value in data.items():
        column_check(table, key)
        columns.append(key)
        values.append(value)
        placeholders.append("%s")

    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)}) RETURNING *"
    conn.cur.execute(sql, values)
    result = conn.cur.fetchone()
    if result is None:
        raise RuntimeError("Insert operation failed, no row returned")
    return result


def update(table, data, conditions):
    table_check(table)
    data_check("Update", data)
    conditions_check("Update", conditions)

    set_clauses = []
    where_clauses = []
    params = []

    for col, val in data.items():
        column_check(table, col)
        set_clauses.append(f"{col} = %s")
        params.append(val)

    for col, val in conditions.items():
        column_check(table, col)
        where_clauses.append(f"{col} = %s")
        params.append(val)

    sql = f"""
        UPDATE {table}
        SET {', '.join(set_clauses)}
        WHERE {' AND '.join(where_clauses)}
        RETURNING *
    """
    conn.cur.execute(sql, params)
    row = conn.cur.fetchone()
    if row is None:
        raise RuntimeError("Update operation failed, no row returned")
    return row


def fetch(table, conditions=None, order_by=None):
    table_check(table)
    sql = f"SELECT * FROM {table}"
    sql, params = join_conditions(sql, table, conditions)
    if order_by:
        sql += f" ORDER BY {order_by}"
        
    conn.cur.execute(sql, params)
    return conn.cur.fetchall()


def fetch_in(table, column, values, order_by=None):
    """查詢符合 IN 條件的記錄
    
    Args:
        table: 表名
        column: 欄位名（如 'product_id'）
        values: 值的列表（如 [1, 2, 3, 4]）
        order_by: 排序欄位（可選）
    
    Returns:
        list: 查詢結果
    
    Example:
        fetch_in("PRODUCT", "product_id", [1, 2, 3])
        # 生成 SQL: SELECT * FROM PRODUCT WHERE product_id IN (1, 2, 3)
    """
    table_check(table)
    column_check(table, column)
    
    if not values:
        return []
    
    # 生成 SQL
    placeholders = ','.join(['%s'] * len(values))
    sql = f"SELECT * FROM {table} WHERE {column} IN ({placeholders})"
    
    if order_by:
        sql += f" ORDER BY {order_by}"
    
    conn.cur.execute(sql, values)
    return conn.cur.fetchall()


def selective_fetch(table, columns, conditions=None, order_by=None):
    """選擇性查詢特定欄位
    
    Args:
        table: 表名
        columns: 欄位列表（如 ['user_id', 'user_name']）
        conditions: 查詢條件字典（如 {'user_id': 1}）
        order_by: 排序欄位（可選）
    
    Returns:
        list: 查詢結果
    """
    table_check(table)
    for col in columns:
        column_check(table, col)

    sql = f"SELECT {', '.join(columns)} FROM {table}"
    
    # ✅ 修正：確保 conditions 是字典
    if conditions:
        sql, params = join_conditions(sql, table, conditions)
    else:
        params = []
    
    if order_by:
        sql += f" ORDER BY {order_by}"

    conn.cur.execute(sql, params)
    return conn.cur.fetchall()


def exists(table, conditions=None) -> bool:
    table_check(table)
    sql = f"SELECT 1 FROM {table}"
    sql, params = join_conditions(sql, table, conditions)
    conn.cur.execute(sql, params)
    return conn.cur.fetchone() is not None


def delete(table, conditions):
    table_check(table)
    conditions_check("DELETE", conditions)
    sql = f"DELETE FROM {table}"
    sql, params = join_conditions(sql, table, conditions)
    conn.cur.execute(sql, params)
    return conn.cur.rowcount


def lock_rows(table, conditions):
    table_check(table)
    conditions_check("Lock Rows", conditions)
    sql = f"SELECT * FROM {table}"
    sql, params = join_conditions(sql, table, conditions)
    sql += " FOR UPDATE"
    conn.cur.execute(sql, params)
    return conn.cur.fetchall()