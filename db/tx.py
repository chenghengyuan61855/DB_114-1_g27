from contextlib import contextmanager
from db import conn
import psycopg2

@contextmanager
def transaction():
    """
    用法：
        from db.tx import transaction

        def db_place_order(...):
            with transaction():
                lock_rows(...)
                insert(...)
                update(...)
    """
    # ✅ 如果當前交易有錯誤，先 rollback
    try:
        # 測試當前交易狀態
        if conn.db and not conn.db.closed:
            conn.cur.execute("SELECT 1")
            conn.cur.fetchone()
    except psycopg2.Error:
        # 有錯誤就 rollback
        if conn.db and not conn.db.closed:
            conn.db.rollback()
    
    old_autocommit = conn.db.autocommit
    
    # ✅ 不要改變 autocommit（已經是 False）
    # conn.db.autocommit = False  # ← 移除這行
    
    try:
        yield # 在此區塊內執行的所有操作都在同一個交易中
        conn.db.commit()
    except Exception:
        conn.db.rollback() 
        raise
    finally:
        # ✅ 恢復原始設定（但由於我們沒改，這裡也不用做事）
        pass  # conn.db.autocommit = old_autocommit
