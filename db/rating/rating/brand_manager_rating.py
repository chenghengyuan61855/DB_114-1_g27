# ui/rating/brand_manager_rating.py
from db.rating.fetch import (
    db_fetch_brand_ratings,
    db_fetch_product_ratings,
    db_fetch_low_rated_products,
    db_fetch_rating_statistics,
    db_fetch_top_rated_products
)
from ui.helper import clear_screen


def ui_view_all_ratings(brand_id):
    """查看品牌下所有評價"""
    clear_screen()
    print("\n=== 品牌所有評價 ===")
    
    try:
        ratings = db_fetch_brand_ratings(brand_id)
        
        if not ratings:
            print("目前沒有任何評價")
            return
        
        print(f"共 {len(ratings)} 筆評價\n")
        
        for idx, rating in enumerate(ratings, 1):
            print(f"\n{'='*60}")
            print(f"[{idx}] 商品：{rating['product_name']} (ID: {rating['product_id']})")
            print(f"門市：{rating['store_name']} (ID: {rating['store_id']})")
            print(f"評分：{'⭐' * rating['rating']} ({rating['rating']}/5)")
            
            if rating['comment']:
                print(f"評論：{rating['comment']}")
            else:
                print("評論：（無）")
            
            print(f"時間：{rating['created_at']}")
            print(f"訂單編號：{rating['order_id']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_product_ratings(product_id):
    """查看特定商品的評價"""
    clear_screen()
    print(f"\n=== 商品 {product_id} 的評價 ===")
    
    try:
        ratings = db_fetch_product_ratings(product_id)
        
        if not ratings:
            print("此商品目前沒有評價")
            return
        
        avg_rating = sum(r['rating'] for r in ratings) / len(ratings)
        
        print(f"評價數量：{len(ratings)} 筆")
        print(f"平均評分：{avg_rating:.2f} / 5.0")
        print(f"{'='*60}\n")
        
        for idx, rating in enumerate(ratings, 1):
            print(f"\n[{idx}] {'⭐' * rating['rating']} ({rating['rating']}/5)")
            
            if rating['comment']:
                print(f"評論：{rating['comment']}")
            else:
                print("評論：（無）")
            
            print(f"時間：{rating['created_at']}")
            print(f"訂單：{rating['order_id']} | 門市：{rating['store_id']}")
            print(f"-"*60)
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_low_rated_products(brand_id, threshold=3):
    """查看低評分商品"""
    clear_screen()
    print(f"\n=== 低評分商品（平均 < {threshold} 星）===")
    
    try:
        products = db_fetch_low_rated_products(brand_id, threshold)
        
        if not products:
            print(f"✅ 太棒了！沒有商品的平均評分低於 {threshold} 星")
            return
        
        print(f"⚠️ 發現 {len(products)} 個需要改進的商品\n")
        print(f"{'商品 ID':<10} {'商品名稱':<20} {'評價數':<10} {'平均分':<10} {'最低分':<10}")
        print("="*70)
        
        for p in products:
            print(f"{p['product_id']:<10} {p['product_name']:<20} "
                  f"{p['rating_count']:<10} {p['avg_rating']:<10.2f} {p['min_rating']:<10}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_rating_statistics(brand_id):
    """查看評價統計"""
    clear_screen()
    print("\n=== 品牌評價統計 ===")
    
    try:
        stats = db_fetch_rating_statistics(brand_id)
        
        if not stats or stats['total_ratings'] == 0:
            print("目前沒有任何評價資料")
            return
        
        print(f"\n{'='*60}")
        print(f"商品總數：{stats['total_products']} 個")
        print(f"評價總數：{stats['total_ratings']} 筆")
        print(f"整體平均評分：{stats['overall_avg_rating']:.2f} / 5.0")
        print(f"{'='*60}\n")
        
        print("評分分布：")
        total = stats['total_ratings']
        
        print(f"⭐⭐⭐⭐⭐ 5 星：{stats['five_star']:>4} 筆 "
              f"({stats['five_star']/total*100:>5.1f}%)")
        
        print(f"⭐⭐⭐⭐   4 星：{stats['four_star']:>4} 筆 "
              f"({stats['four_star']/total*100:>5.1f}%)")
        
        print(f"⭐⭐⭐     3 星：{stats['three_star']:>4} 筆 "
              f"({stats['three_star']/total*100:>5.1f}%)")
        
        print(f"⭐⭐       2 星：{stats['two_star']:>4} 筆 "
              f"({stats['two_star']/total*100:>5.1f}%)")
        
        print(f"⭐         1 星：{stats['one_star']:>4} 筆 "
              f"({stats['one_star']/total*100:>5.1f}%)")
        
        satisfied = stats['five_star'] + stats['four_star']
        satisfaction_rate = satisfied / total * 100
        
        print(f"\n{'='*60}")
        print(f"顧客滿意度（4-5 星）：{satisfaction_rate:.1f}%")
        print(f"{'='*60}\n")
        
        print("=== 高評分商品 TOP 5 ===")
        top_products = db_fetch_top_rated_products(brand_id, limit=5)
        
        if top_products:
            print(f"{'商品名稱':<30} {'評價數':<10} {'平均分':<10}")
            print("-"*60)
            for p in top_products:
                print(f"{p['product_name']:<30} {p['rating_count']:<10} "
                      f"{p['avg_rating']:.2f}")
        else:
            print("（暫無足夠評價的商品）")
    
    except Exception as e:
        print(f"❌ Error: {e}")
