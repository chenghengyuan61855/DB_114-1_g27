from contextlib import contextmanager
from db import conn

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
    old_autocommit = conn.db.autocommit
    conn.db.autocommit = False
    try:
        yield # 在此區塊內執行的所有操作都在同一個交易中
        conn.db.commit()
    except Exception:
        conn.db.rollback() 
        raise
    finally:
        conn.db.autocommit = old_autocommit
