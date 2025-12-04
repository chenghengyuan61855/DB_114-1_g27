import hashlib

def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def cancel_check(input_str: str, ui_type: str) -> bool:
    if input_str.strip() == ":q":
        print(f"{ui_type} cancelled.")
        return True
    return False