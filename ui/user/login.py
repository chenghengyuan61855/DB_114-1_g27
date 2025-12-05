from db.crud import exists
from db.user.login import db_login_user
from ui.helper import cancel_check
from ui.user.helper import hash_pwd, phone_check, password_check

def ui_login_user():
    print("=== User Login ===")
    print("(Type ':q' in any input to cancel login)\n")
    # -------- Phone --------
    while True:
        user_phone = input("Enter phone number (09xxxxxxxx): ").strip()
        if(cancel_check(user_phone, "Login")):
            return
        
        if not phone_check(user_phone):
            continue

        if not exists("APP_USER", {"user_phone": user_phone}):
            print("❌ Phone number not registered.")
            print("If you don't have an account, please type ':q' to cancel and create a new user.")
            continue

        break
    
    # -------- Password --------
    while True:
        password = input("Enter password: ").strip()
        if cancel_check(password, "Login"):
            return
    
        if not password_check(password):
            continue

        password_hash = hash_pwd(password)
        user_id = db_login_user(user_phone, password_hash)

        if user_id is None:
            print("❌ Incorrect password. Please try again.")
            continue

        print(f"\n✅ Login successful! User ID: {user_id}")
        return user_id