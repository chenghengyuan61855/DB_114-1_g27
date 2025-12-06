# ui/product/create.py
from db.product.create import db_create_product
from ui.helper import cancel_check

def ui_create_product(brand_id):
    """UI：建立新商品"""
    print("\n=== Create Product ===")
    
    product_name = input("Product Name: ").strip()
    if cancel_check(product_name, "Product Creation"):
        return
    
    size = input("Size (optional): ").strip() or None
    product_description = input("Description: ").strip() or None
    
    try:
        product_id = db_create_product(
            brand_id, 
            p_category_id=None,
            product_name=product_name,
            size=size,
            product_description=product_description,
            image_url=None
        )
        print(f"✅ Product created with ID: {product_id}")
        return product_id
    except Exception as e:
        print(f"❌ Error: {e}")