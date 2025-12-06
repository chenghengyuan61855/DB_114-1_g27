from db.user.profile import db_view_user_profile, db_update_user_profile
from ui.helper import cancel_check
from ui.user.helper import name_check, email_check, password_check, hash_pwd

def ui_view_user_profile(user_id):
    profile = db_view_user_profile(user_id)
    if not profile:
        print("Profile not found.")
        return
    
    print("User Profile:")
    print(f"ID: {profile['user_id']}")
    print(f"Name: {profile['user_name']}")
    print(f"Email: {profile['user_email']}")
    print(f"Phone: {profile['user_phone']}")
    print(f"Active: {profile['is_active']}")

def ui_update_user_profile(user_id):
    print("=== Update User Profile ===")
    print("(Leave blank to keep current value)")
    print("(Type ':q' in any input to cancel profile update)")
   
    profile = db_view_user_profile(user_id)
    if not profile:
        print("Profile not found.")
        return
    

    print(f"Current Name: {profile['user_name']}")
    while True:
        new_name = input("New Name: ").strip()
        if cancel_check(new_name, "Profile Update"):
            return
        
        if new_name == '':
            new_name = profile['user_name']
            break

        if not name_check(new_name):
            continue

        name_confirm = input(f"Confirm New Name '{new_name}'? (y/n): ").strip().lower()
        if name_confirm == 'y':
            break
        elif name_confirm == 'n':
            print("Let's try again.")

    print(f"Current Email: {profile['user_email']}")
    while True:
        new_email = input("New Email: ").strip()
        if cancel_check(new_email, "Profile Update"):
            return
        
        if new_email == '':
            new_email = profile['user_email']
            break

        if not email_check(new_email):
            continue

        email_confirm = input(f"Confirm New Email '{new_email}'? (y/n): ").strip().lower()
        if email_confirm == 'y':
            break
        elif email_confirm == 'n':
            print("Let's try again.")

        
    while True:
        pwd_confirm = input("Enter your password to confirm changes: ")
        if not password_check(pwd_confirm):
            continue

        if hash_pwd(pwd_confirm) != profile.get('password_hash'):
            print("❌ Incorrect password. Please try again.")
            continue

        break

    updates = {
        "user_name": new_name,
        "user_email": new_email,
    }

    updated_rows = db_update_user_profile(user_id, updates)
    if updated_rows:
        print("✅ Profile updated successfully.")
    else:
        print("❌ Profile update failed.")