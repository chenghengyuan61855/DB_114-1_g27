#!/usr/bin/env python3
"""
測試 NoSQL 點擊記錄功能
"""

from db.nosql_logger import log_drink_click, mark_drink_as_submitted
from pymongo import MongoClient
from datetime import datetime

def test_click_logging():
    """測試點擊記錄功能"""
    
    print("\n=== 測試 NoSQL 點擊記錄功能 ===\n")
    
    # 連接 MongoDB（使用正確的資料庫名稱）
    client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=2000)
    db = client['nosql_database']  # ← 修正：使用 nosql_database
    
    # 清理測試資料
    db.drink_clicks.delete_many({'user_id': 888})
    print("✅ 清理舊測試資料")
    
    # 測試 1: 記錄點擊
    print("\n--- 測試 1: 記錄點擊 ---")
    log_drink_click(user_id=888, brand_id=2, product_id=11)
    log_drink_click(user_id=888, brand_id=2, product_id=12)
    log_drink_click(user_id=888, brand_id=2, product_id=11)  # 重複點擊
    
    clicks = list(db.drink_clicks.find({'user_id': 888}))
    print(f"✅ 記錄了 {len(clicks)} 筆點擊")
    for click in clicks:
        print(f"   - Product {click['product_id']}, Submitted: {click['submitted']}")
    
    # 測試 2: 標記為已提交
    print("\n--- 測試 2: 標記訂單為已提交 ---")
    mark_drink_as_submitted(user_id=888, brand_id=2, product_id=11, order_id=99999)
    
    clicks_after = list(db.drink_clicks.find({'user_id': 888}))
    submitted_count = sum(1 for c in clicks_after if c['submitted'])
    print(f"✅ 已提交的點擊: {submitted_count} 筆")
    
    for click in clicks_after:
        status = "✅ 已提交" if click['submitted'] else "⏳ 未提交"
        print(f"   - Product {click['product_id']}: {status}")
    
    # 測試 3: 查看所有資料
    print("\n--- 測試 3: 查看所有點擊資料 ---")
    all_clicks = list(db.drink_clicks.find().limit(20))
    print(f"✅ 資料庫共有 {db.drink_clicks.count_documents({})} 筆點擊記錄")
    
    if all_clicks:
        print("\n最近 20 筆記錄:")
        for click in all_clicks:
            status = "✅" if click['submitted'] else "⏳"
            print(f"   {status} User {click['user_id']}, Brand {click['brand_id']}, Product {click['product_id']}")
    
    # 清理測試資料
    print("\n--- 清理測試資料 ---")
    db.drink_clicks.delete_many({'user_id': 888})
    print("✅ 測試資料已清理")
    
    print("\n=== 測試完成 ===\n")

if __name__ == "__main__":
    test_click_logging()
