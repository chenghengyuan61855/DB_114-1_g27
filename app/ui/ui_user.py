from app.db.db_common import insert, update, fetch, exists, delete
from app.db.db_user import create_user, login_user
from app.ui.ui_helper import hash_pwd, cancel_check

def name_check(user_name: str) -> bool:
    if "\\" in user_name:
        print("❌ Invalid character '\\' in user name.")
        return False

    if not (3 <= len(user_name) <= 20):
        print("❌ User name must be 3–20 characters.")
        return False

    return True

def phone_check(user_phone: str) -> bool:
    if "\\" in user_phone:
        print("❌ Invalid character '\\' in phone number.")
        return False

    if len(user_phone) != 10 or not user_phone.isdigit() or not user_phone.startswith("09"):
        print("❌ Invalid phone number format, expected 10 digits starting with '09'.")
        return False
    
    return True

def password_check(password: str) -> bool:
    if "\\" in password:
        print("❌ Invalid character '\\' in password.")
        return False

    if len(password) < 6:
        print("❌ Password must be at least 6 characters.")
        return False

    return True

def email_check(user_email: str) -> bool:
    if "\\" in user_email:
        print("❌ Invalid character '\\' in email.")
        return False

    if len(user_email) > 50:
        print("❌ Email too long (max 50 characters).")
        return False

    if "@" not in user_email or "." not in user_email.split("@")[-1]:
        print("❌ Invalid email format.")
        return False

    return True

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

        if not exists("app_user", {"user_phone": user_phone}):
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
        user_id = login_user(user_phone, password_hash)

        if user_id is None:
            print("❌ Incorrect password. Please try again.")
            continue

        print(f"\n✅ Login successful! User ID: {user_id}")
        return user_id
    
def ui_create_user():
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
            if exists("app_user", {"user_phone": user_phone}):
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

        if exists("app_user", {"user_email": user_email}):
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
        user_id = create_user(user_name, user_email, user_phone, password_hash)
        print(f"\n✅ User created with ID: {user_id}")
    except ValueError as ve:
        print(f"❌ Error: {ve}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
