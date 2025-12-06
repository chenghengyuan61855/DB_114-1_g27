# db/crud.py
from db import conn
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

def fetch(table, conditions=None):
    table_check(table)
    sql = f"SELECT * FROM {table}"
    sql, params = join_conditions(sql, table, conditions)
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