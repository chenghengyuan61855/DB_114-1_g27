import hashlib

def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
def allowed_chars_check(input_str: str) -> bool:
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!.@#$%^&*()-_=+`~")
    for char in input_str:
        if char not in allowed_chars:
            print(f"❌ Invalid character detected: '{char}'")
            print("Allowed characters are letters, digits, and !@#$%^&*()-_=+`~")
            return False
    return True

def name_check(user_name: str) -> bool:
    if not allowed_chars_check(user_name):
        return False

    if not (3 <= len(user_name) <= 20):
        print("❌ User name must be 3–20 characters.")
        return False

    return True

def phone_check(user_phone: str) -> bool:
    if len(user_phone) != 10 or not user_phone.isdigit() or not user_phone.startswith("09"):
        print("❌ Invalid phone number format, expected 10 digits starting with '09'.")
        return False
    
    return True

def password_check(password: str) -> bool:
    if not allowed_chars_check(password):
        return False

    if len(password) < 6:
        print("❌ Password must be at least 6 characters.")
        return False

    return True

def email_check(user_email: str) -> bool:
    if not allowed_chars_check(user_email):
        return False

    if len(user_email) > 50:
        print("❌ Email too long (max 50 characters).")
        return False

    if "@" not in user_email or "." not in user_email.split("@")[-1]:
        print("❌ Invalid email format.")
        return False

    return True