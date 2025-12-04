import hashlib

def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

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