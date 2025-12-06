from db.crud import fetch

def db_show_brand_list():
    brands = fetch("BRAND", {})
    brands_list = []
    for row in brands:
        if row[5]:
            brand_info = {
                "brand_id": row[0],
                "brand_name": row[1],
            }
            brands_list.append(brand_info)
    brands_list.sort(key=lambda x: x["brand_id"])
    print("\nAvailable Brands:")
    for brand in brands_list:
        print(f"ID: {brand['brand_id']}, Name: {brand['brand_name']}")