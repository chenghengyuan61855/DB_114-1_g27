from db.conn import connect, close
from ui.main import run

def main():
    connect()
    try: 
        run()
    finally:
        close()

if __name__ == "__main__":
    main()