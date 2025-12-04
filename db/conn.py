import psycopg2
import os
from dotenv import load_dotenv

DB_NAME = "DaTeabase"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

def _get_db_password():
    load_dotenv()
    pwd = os.getenv("DB_PASSWORD")
    if not pwd:
        raise RuntimeError("DB_PASSWORD is not set")
    return pwd

db = None
cur = None

def connect():
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