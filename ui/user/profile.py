from db.user.profile import db_view_user_profile, db_update_user_profile

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
    print("--- Update User Profile ---")
    print("(Leave blank to keep current value)")
    print("(Type ':q' in any input to cancel profile update)")
    
    print("Current Profile:")
    profile = db_view_user_profile(user_id)
    if not profile:
        print("Profile not found.")
        return
    
    new_name = input("Enter new name: ").strip()
    new_email = input("Enter new email: ").strip()
    
    updates = {}
    if new_name:
        updates["user_name"] = new_name
    if new_email:
        updates["user_email"] = new_email
    
    if updates:
        db_update_user_profile(user_id, updates)
        print("Profile updated successfully.")
    else:
        print("No changes made to the profile.")