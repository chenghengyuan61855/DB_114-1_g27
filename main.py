from db.conn import connect, close
from ui.main import run
from ui.helper import clear_screen

def main():
    clear_screen()
    connect()
    try: 
        run()
    finally:
        close()

if __name__ == "__main__":
    main()