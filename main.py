from app.db.db_conn import connect, close
from app.ui.ui_main import run

def main():
    connect()
    run()
    close()

if __name__ == "__main__":
    main()