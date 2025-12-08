from db.nosql_analytics import (
    get_product_click_stats,
    get_top_products,
    get_high_abandon_products,
    get_conversion_rate,
    get_hourly_click_distribution
)
from db.product.fetch import db_fetch_product
from ui.helper import clear_screen


# 中文對齊輔助函數
def get_display_width(text):
    """計算字串顯示寬度（中文字算2個字元，英文算1個）"""
    width = 0
    for char in str(text):
        # 判斷是否為中文字符（包括中文標點符號）
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f':
            width += 2
        else:
            width += 1
    return width


def pad_string(text, target_width):
    """將字串填充到指定顯示寬度"""
    current_width = get_display_width(text)
    padding = target_width - current_width
    return text + ' ' * max(0, padding)


def ui_view_click_analytics(brand_id):
    """品牌飲料點擊分析主選單"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("=== 飲料點擊分析 ===".center(60))
        print("="*60)
        print(f"Brand ID: {brand_id}")
        print("="*60)
        
        print("\n1. 查看商品點擊統計")
        print("2. 查看熱門商品 TOP 10")
        print("3. 查看高反悔率商品")
        print("4. 查看整體轉換率")
        print("5. 查看熱門時段分析")
        print("q. 返回上一層")
        print("="*60)
        
        command = input("\n請輸入指令: ").strip()
        
        if command == "1":
            ui_view_product_click_stats(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "2":
            ui_view_top_products(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "3":
            ui_view_high_abandon_products(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "4":
            ui_view_conversion_rate(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "5":
            ui_view_hourly_distribution(brand_id)
            input("\n按 Enter 繼續...")
        
        elif command == "q":
            return
        
        else:
            print("❌ 無效的指令")
            input("\n按 Enter 繼續...")


def ui_view_product_click_stats(brand_id):
    """查看商品點擊統計"""
    clear_screen()
    print("\n=== 商品點擊統計（最近 30 天）===\n")
    
    days = input("查詢天數（預設 30 天，直接按 Enter 使用預設）: ").strip()
    days = int(days) if days.isdigit() else 30
    
    try:
        stats = get_product_click_stats(brand_id, days)
        
        if not stats:
            print("⚠️ 目前沒有點擊資料")
            return
        
        # 批次查詢商品名稱
        product_ids = [s["product_id"] for s in stats]
        products = db_fetch_product(brand_id=brand_id)
        product_map = {p["product_id"]: p["product_name"] for p in products}
        
        print(f"\n共 {len(stats)} 個商品有點擊記錄\n")
        print(f"{pad_string('商品ID', 12)}{pad_string('商品名稱', 32)}{pad_string('總點擊', 12)}{pad_string('完成訂單', 14)}{pad_string('反悔率', 12)}")
        print("="*82)
        
        for s in stats:
            product_id = s["product_id"]
            product_name = product_map.get(product_id, "Unknown")
            total_clicks = s["total_clicks"]
            submitted = s["submitted_count"]
            abandon_rate = s["abandon_rate"]
            
            print(f"{pad_string(str(product_id), 12)}{pad_string(product_name, 32)}{pad_string(str(total_clicks), 12)}"
                  f"{pad_string(str(submitted), 14)}{pad_string(f'{abandon_rate:.2f}%', 12)}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_top_products(brand_id):
    """查看熱門商品"""
    clear_screen()
    print("\n=== 熱門商品 TOP 10（最近 30 天）===\n")
    
    try:
        top_products = get_top_products(brand_id, days=30, limit=10)
        
        if not top_products:
            print("⚠️ 目前沒有點擊資料")
            return

        # 批次查詢商品名稱
        products = db_fetch_product(brand_id=brand_id)
        product_map = {p["product_id"]: p["product_name"] for p in products}

        # 表頭（使用顯示寬度對齊商品名稱欄位）
        print(f"{pad_string('排名', 10)}{pad_string('商品名稱', 32)}{pad_string('點擊次數', 14)}{pad_string('完成訂單', 14)}{pad_string('轉換率', 12)}")
        print("=" * 82)

        for idx, s in enumerate(top_products, 1):
            product_id = s["product_id"]
            product_name = product_map.get(product_id, "Unknown")
            total_clicks = s["total_clicks"]
            submitted = s["submitted_count"]
            conversion = (submitted / total_clicks * 100) if total_clicks > 0 else 0

            print(f"{pad_string(str(idx), 10)}{pad_string(product_name, 32)}{pad_string(str(total_clicks), 14)}"
                  f"{pad_string(str(submitted), 14)}{pad_string(f'{conversion:.1f}%', 12)}")
        
        print("\n提示：點擊次數高代表商品有吸引力，轉換率低可能需要改善定價或描述")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_high_abandon_products(brand_id):
    """查看高反悔率商品"""
    clear_screen()
    print("\n=== 高反悔率商品（最近 30 天）===\n")
    
    threshold = input("反悔率門檻（預設 50%，直接按 Enter 使用預設）: ").strip()
    threshold = float(threshold) if threshold.replace('.', '').isdigit() else 50.0
    
    try:
        high_abandon = get_high_abandon_products(brand_id, days=30, threshold=threshold)
        
        if not high_abandon:
            print(f"✅ 太棒了！沒有商品的反悔率超過 {threshold}%")
            return
        
        # 批次查詢商品名稱
        products = db_fetch_product(brand_id=brand_id)
        product_map = {p["product_id"]: p["product_name"] for p in products}
        
        print(f"⚠️ 發現 {len(high_abandon)} 個高反悔率商品（> {threshold}%）\n")
        print(f"{pad_string('商品名稱', 32)}{pad_string('總點擊', 12)}{pad_string('完成訂單', 14)}{pad_string('反悔率', 12)}")
        print("="*70)
        
        for s in high_abandon:
            product_id = s["product_id"]
            product_name = product_map.get(product_id, "Unknown")
            total_clicks = s["total_clicks"]
            submitted = s["submitted_count"]
            abandon_rate = s["abandon_rate"]
            
            print(f"{pad_string(product_name, 32)}{pad_string(str(total_clicks), 12)}"
                  f"{pad_string(str(submitted), 14)}{pad_string(f'{abandon_rate:.1f}%', 12)}")
        
        print("\n提示：高反悔率可能代表價格過高、描述不清楚或選項設定有問題")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_conversion_rate(brand_id):
    """查看整體轉換率"""
    clear_screen()
    print("\n=== 品牌整體轉換率（最近 30 天）===\n")
    
    try:
        stats = get_conversion_rate(brand_id, days=30)
        
        total_clicks = stats["total_clicks"]
        total_orders = stats["total_orders"]
        conversion_rate = stats["conversion_rate"]
        
        print(f"總點擊次數：{total_clicks}")
        print(f"完成訂單數：{total_orders}")
        print(f"整體轉換率：{conversion_rate:.2f}%")
        
        print("\n" + "="*60)
        
        # 轉換率評估
        if conversion_rate >= 70:
            print("✅ 優秀！轉換率非常高")
        elif conversion_rate >= 50:
            print("👍 良好！轉換率在正常範圍")
        elif conversion_rate >= 30:
            print("⚠️ 需要改進！轉換率偏低")
        else:
            print("❌ 警告！轉換率過低，建議檢查商品設定和使用者體驗")
        
        print("="*60)
        
        print("\n提示：")
        print("  • 轉換率低可能原因：商品價格過高、選項設定複雜、結帳流程不順暢")
        print("  • 可以查看「高反悔率商品」找出問題商品")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def ui_view_hourly_distribution(brand_id):
    """查看熱門時段分析"""
    clear_screen()
    print("\n=== 熱門時段分析（最近 7 天）===\n")
    
    try:
        hourly_dist = get_hourly_click_distribution(brand_id, days=7)
        
        total_clicks = sum(hourly_dist.values())
        
        if total_clicks == 0:
            print("⚠️ 目前沒有點擊資料")
            return
        
        print("點擊次數分布（每小時）：\n")
        print(f"{'時段':<10} {'點擊次數':<12} {'佔比':<10} {'視覺化'}")
        print("="*60)
        
        for hour in range(24):
            count = hourly_dist[hour]
            percentage = (count / total_clicks * 100) if total_clicks > 0 else 0
            bar = "█" * int(percentage / 2)  # 每 2% 一個方塊
            
            time_range = f"{hour:02d}:00-{hour:02d}:59"
            print(f"{time_range:<10} {count:<12} {percentage:<10.1f}% {bar}")
        
        # 找出熱門時段（前 3 名）
        top_hours = sorted(hourly_dist.items(), key=lambda x: x[1], reverse=True)[:3]
        
        print("\n" + "="*60)
        print("熱門時段 TOP 3：")
        for idx, (hour, count) in enumerate(top_hours, 1):
            print(f"  {idx}. {hour:02d}:00-{hour:02d}:59 - {count} 次點擊")
        
        # print("\n提示：可在熱門時段推出限時優惠或增加人力準備")
    
    except Exception as e:
        print(f"❌ Error: {e}")
