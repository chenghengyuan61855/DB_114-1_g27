from db.crud import exists
from db.user.create import db_create_user
from ui.helper import cancel_check
from ui.user.helper import hash_pwd, name_check, phone_check, email_check, password_check
from ui.helper import clear_screen  # ← 導入 clear_screen



def ui_create_user():
    clear_screen()  # ← 在創建用戶介面前清屏
    print("\n=== Create User ===")
    print("(Type ':q' in any input to cancel user creation)\n")

    # -------- user_name--------
    while True:
        user_name = input("Enter user name: ").strip()
        if cancel_check(user_name, "User Creation"):
            return
        
        if name_check(user_name):
            break

    # -------- Phone --------
    while True:
        user_phone = input("Enter phone number (09xxxxxxxx): ").strip()
        if cancel_check(user_phone, "User Creation"):
            return

        if phone_check(user_phone):
            if exists("APP_USER", {"user_phone": user_phone}):
                print("❌ Phone number already registered.")
                continue
            break
    
    # -------- Email --------
    while True:
        user_email = input("Enter user email: (leave blank and press enter to skip)").strip()
        if cancel_check(user_email, "User Creation"):
            return
        
        if user_email == "":
            user_email = None
            break
            
        if not email_check(user_email):
            continue

        if exists("APP_USER", {"user_email": user_email}):
            print("❌ Email already registered.")
            continue

        break

    # -------- Password --------
    while True:
        password = input("Enter password: ")
        if cancel_check(password, "User Creation"):
            return

        if not password_check(password):
            continue

        confirm = input("Enter password again to confirm: ")
        if confirm != password:
            print("❌ Passwords do not match. Please try again.")
            continue

        break

    password_hash = hash_pwd(password)

    # -------- DB input --------
    try:
        user_id = db_create_user(user_name, user_email, user_phone, password_hash)
        print(f"\n✅ User created with ID: {user_id}")
    except ValueError as ve:
        print(f"❌ Error: {ve}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # ← 加這一行（無論成功或失敗都暫停）
    # input("\n按 Enter 繼續...") 不需要加，因為 ui/main.py 已經有了