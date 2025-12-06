from db.crud import fetch

def ui_show_brand_list():
    brands = fetch("BRAND", {"is_active": True})
    print("\nAvailable Brands:")
    for brand in brands:
        print(f"{brand[0]}. {brand[1]}")
    return brands
    