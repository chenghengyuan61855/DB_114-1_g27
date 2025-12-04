from db import conn
from db.allowed import ALLOWED_TABLES, ALLOWED_COLUMNS

def table_check(table):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table: {table}")
    
def column_check(table, column):
    if column not in ALLOWED_COLUMNS[table]:
        raise ValueError(f"Invalid column '{column}' for table '{table}'")

def data_check(op_type:str , data):
    if not data:
        raise ValueError(f"{op_type} data cannot be empty")

def conditions_check(op_type:str , conditions):
    if not conditions:
        raise ValueError(f"{op_type} without conditions is not allowed")

def fetch(table, conditions=None):
    table_check(table)

    sql = f"SELECT * FROM {table}"
    params = [] 
    
    if conditions:
        clauses = []
        for key, value in conditions.items():
            column_check(table, key)
            clauses.append(f"{key} = %s")
            params.append(value)
        sql += " WHERE " + " AND ".join(clauses)

    conn.cur.execute(sql, params)
    return conn.cur.fetchall()

def insert(table, data):
    table_check(table)
    data_check("Insert", data)

    columns = []
    values = []
    placeholders = []

    for key, value in data.items():
        if key not in ALLOWED_COLUMNS[table]:
            raise ValueError(f"Invalid column '{key}' for table '{table}'")
        columns.append(key)
        values.append(value)
        placeholders.append("%s")

    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)}) RETURNING *"
    conn.cur.execute(sql, values)
    result = conn.cur.fetchone()
    if result is None:
        conn.rollback()
        raise RuntimeError("Insert operation failed, no row returned")
    conn.commit()
    return result

def delete(table, conditions):
    table_check(table)
    conditions_check("DELETE", conditions)

    sql = f"DELETE FROM {table}"
    params = []
    clauses = []

    for key, value in conditions.items():
        if key not in ALLOWED_COLUMNS[table]:
            raise ValueError(f"Invalid column '{key}' for table '{table}'")
        clauses.append(f"{key} = %s")
        params.append(value)

    sql += " WHERE " + " AND ".join(clauses)
    conn.cur.execute(sql, params)
    conn.commit()

def exists(table, conditions) -> bool:
    table_check(table)

    sql = f"SELECT 1 FROM {table}"
    params = []
    
    if conditions:
        clauses = []    
        for key, value in conditions.items():
            column_check(table, key)
            clauses.append(f"{key} = %s")
            params.append(value)
        sql += " WHERE " + " AND ".join(clauses)

    conn.cur.execute(sql, params)
    return conn.cur.fetchone() is not None

def update(table, data, conditions):
    table_check(table)
    data_check("Update", data)
    conditions_check("Update", conditions)

    set_clauses = []
    where_clauses = []
    params = []

    # SET
    for col, val in data.items():
        column_check(table, col)
        set_clauses.append(f"{col} = %s")
        params.append(val)

    # WHERE
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
    conn.commit()
    return row