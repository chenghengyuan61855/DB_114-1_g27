import psycopg2
import psycopg2.pool
import os
from dotenv import load_dotenv

DB_NAME = "daTEAbase"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

def _get_db_password():
    load_dotenv()
    pwd = os.getenv("DB_PASSWORD")
    if not pwd:
        raise RuntimeError("DB_PASSWORD is not set")
    return pwd

# ============================================
# 舊版單一連線模式（向後兼容）
# ============================================
db = None
cur = None

def connect():
    """建立單一資料庫連線（舊版模式，保留向後兼容）"""
    global db, cur
    try:
        DB_PASSWORD = _get_db_password()
        db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        # ⚠️ 暫時使用 autocommit，避免 transaction 錯誤
        # TODO: 未來所有函數加入完整的 try-except-rollback 後再改為 False
        db.autocommit = True
        cur = db.cursor()
        print("Successfully connected to DBMS.")
    except psycopg2.Error as e:
        print("Error connecting to DBMS:", e)
        raise
    except Exception as e:
        print("Internal error", e)
        raise

def commit():
    if db:
        db.commit()

def close():
    if cur:
        cur.close()
    if db:
        db.close()

def rollback():
    if db:
        db.rollback()

def get_cursor():
    """取得當前 cursor（向後兼容）"""
    return cur

def ensure_transaction_clean():
    """確保 transaction 是乾淨的狀態
    
    如果當前 transaction 有錯誤，自動 rollback
    這個函數可以在每次操作前呼叫，確保不會卡在錯誤狀態
    """
    if db and not db.autocommit:
        try:
            # 嘗試執行一個簡單查詢來測試 transaction 狀態
            cur.execute("SELECT 1")
            cur.fetchone()
        except psycopg2.Error:
            # 如果有錯誤，rollback
            db.rollback()
            print("⚠️  Previous transaction error detected and rolled back")


# ============================================
# 新版 Connection Pool 模式（推薦使用）
# ============================================
connection_pool = None

def init_connection_pool(minconn=1, maxconn=10):
    """初始化連線池
    
    Args:
        minconn: 最小連線數
        maxconn: 最大連線數
    """
    global connection_pool
    try:
        DB_PASSWORD = _get_db_password()
        connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print(f"Connection pool initialized (min={minconn}, max={maxconn})")
    except psycopg2.Error as e:
        print("Error initializing connection pool:", e)
        raise
    except Exception as e:
        print("Internal error:", e)
        raise

def get_connection():
    """從連線池取得一個連線
    
    Returns:
        connection: 資料庫連線物件
    """
    if connection_pool is None:
        init_connection_pool()
    return connection_pool.getconn()

def release_connection(conn):
    """將連線歸還至連線池
    
    Args:
        conn: 要歸還的連線物件
    """
    if connection_pool:
        connection_pool.putconn(conn)

def close_connection_pool():
    """關閉連線池"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        connection_pool = None
        print("Connection pool closed")


# ============================================
# Context Manager（推薦使用）
# ============================================
class DatabaseConnection:
    """資料庫連線的 Context Manager
    
    使用範例：
        with DatabaseConnection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            results = cur.fetchall()
            conn.commit()
    """
    def __init__(self):
        self.conn = None
        self.should_release = False
    
    def __enter__(self):
        self.conn = get_connection()
        self.should_release = True
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is not None:
                # 發生例外時自動 rollback
                self.conn.rollback()
            if self.should_release:
                release_connection(self.conn)
        return False  # 不抑制例外