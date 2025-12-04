import psycopg2
import os

DB_NAME = "DaTeabase"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD") #Powershell: $env:DB_PASSWORD="your_password"
DB_HOST = "localhost"
DB_PORT = 5432

db = None
cur = None

def connect():
    global db, cur
    if DB_PASSWORD is None:
        raise RuntimeError("DB_PASSWORD is not set")
    try:
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