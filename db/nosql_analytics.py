# ============================
# AUTHOR: [Your Team]
# CREATED DATE: 2025-12-08
# PURPOSE: NoSQL 飲料點擊分析模組
# ============================

from db.nosql import drink_clicks
from datetime import datetime, timedelta


def get_product_click_stats(brand_id, days=30):
    """查詢品牌商品的點擊統計（過去 N 天）
    
    Args:
        brand_id: 品牌 ID
        days: 查詢天數（預設 30 天）
    
    Returns:
        list: [
            {
                "product_id": 商品 ID,
                "total_clicks": 總點擊次數,
                "submitted_count": 最終送出訂單次數,
                "abandon_rate": 反悔率 (%)
            }
        ]
    """
    start_date = datetime.now() - timedelta(days=days)
    
    pipeline = [
        # 1. 篩選品牌和時間範圍
        {
            "$match": {
                "brand_id": brand_id,
                "timestamp": {"$gte": start_date}
            }
        },
        # 2. 按商品分組統計
        {
            "$group": {
                "_id": "$product_id",
                "total_clicks": {"$sum": 1},
                "submitted_count": {
                    "$sum": {"$cond": [{"$eq": ["$submitted", True]}, 1, 0]}
                }
            }
        },
        # 3. 計算反悔率
        {
            "$project": {
                "product_id": "$_id",
                "total_clicks": 1,
                "submitted_count": 1,
                "abandon_rate": {
                    "$multiply": [
                        {
                            "$divide": [
                                {"$subtract": ["$total_clicks", "$submitted_count"]},
                                "$total_clicks"
                            ]
                        },
                        100
                    ]
                }
            }
        },
        # 4. 按點擊次數排序
        {"$sort": {"total_clicks": -1}}
    ]
    
    results = list(drink_clicks.aggregate(pipeline))
    
    # 格式化輸出
    return [
        {
            "product_id": r["product_id"],
            "total_clicks": r["total_clicks"],
            "submitted_count": r["submitted_count"],
            "abandon_rate": round(r["abandon_rate"], 2)
        }
        for r in results
    ]


def get_top_products(brand_id, days=30, limit=10):
    """查詢最熱門商品（按點擊次數）
    
    Args:
        brand_id: 品牌 ID
        days: 查詢天數
        limit: 返回前幾名
    
    Returns:
        list: 熱門商品列表（按點擊次數排序）
    """
    stats = get_product_click_stats(brand_id, days)
    return stats[:limit]


def get_high_abandon_products(brand_id, days=30, threshold=50):
    """查詢高反悔率商品
    
    Args:
        brand_id: 品牌 ID
        days: 查詢天數
        threshold: 反悔率門檻 (%)
    
    Returns:
        list: 高反悔率商品列表
    """
    stats = get_product_click_stats(brand_id, days)
    high_abandon = [s for s in stats if s["abandon_rate"] >= threshold]
    return sorted(high_abandon, key=lambda x: x["abandon_rate"], reverse=True)


def get_conversion_rate(brand_id, days=30):
    """計算品牌整體轉換率（點擊 → 下單）
    
    Args:
        brand_id: 品牌 ID
        days: 查詢天數
    
    Returns:
        dict: {
            "total_clicks": 總點擊次數,
            "total_orders": 總訂單數,
            "conversion_rate": 轉換率 (%)
        }
    """
    start_date = datetime.now() - timedelta(days=days)
    
    pipeline = [
        {
            "$match": {
                "brand_id": brand_id,
                "timestamp": {"$gte": start_date}
            }
        },
        {
            "$group": {
                "_id": None,
                "total_clicks": {"$sum": 1},
                "total_orders": {
                    "$sum": {"$cond": [{"$eq": ["$submitted", True]}, 1, 0]}
                }
            }
        }
    ]
    
    result = list(drink_clicks.aggregate(pipeline))
    
    if not result:
        return {
            "total_clicks": 0,
            "total_orders": 0,
            "conversion_rate": 0
        }
    
    r = result[0]
    total_clicks = r["total_clicks"]
    total_orders = r["total_orders"]
    conversion_rate = (total_orders / total_clicks * 100) if total_clicks > 0 else 0
    
    return {
        "total_clicks": total_clicks,
        "total_orders": total_orders,
        "conversion_rate": round(conversion_rate, 2)
    }


def get_user_behavior_analysis(user_id, days=30):
    """分析特定使用者的點擊行為
    
    Args:
        user_id: 使用者 ID
        days: 查詢天數
    
    Returns:
        dict: 使用者行為分析結果
    """
    start_date = datetime.now() - timedelta(days=days)
    
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "timestamp": {"$gte": start_date}
            }
        },
        {
            "$group": {
                "_id": None,
                "total_clicks": {"$sum": 1},
                "unique_products": {"$addToSet": "$product_id"},
                "submitted_count": {
                    "$sum": {"$cond": [{"$eq": ["$submitted", True]}, 1, 0]}
                }
            }
        }
    ]
    
    result = list(drink_clicks.aggregate(pipeline))
    
    if not result:
        return {
            "total_clicks": 0,
            "unique_products_viewed": 0,
            "orders_placed": 0,
            "abandon_rate": 0
        }
    
    r = result[0]
    total_clicks = r["total_clicks"]
    submitted = r["submitted_count"]
    abandon_rate = ((total_clicks - submitted) / total_clicks * 100) if total_clicks > 0 else 0
    
    return {
        "total_clicks": total_clicks,
        "unique_products_viewed": len(r["unique_products"]),
        "orders_placed": submitted,
        "abandon_rate": round(abandon_rate, 2)
    }


def get_hourly_click_distribution(brand_id, days=7):
    """查詢品牌的每小時點擊分布（用於分析熱門時段）
    
    Args:
        brand_id: 品牌 ID
        days: 查詢天數
    
    Returns:
        dict: {小時: 點擊次數}
    """
    start_date = datetime.now() - timedelta(days=days)
    
    pipeline = [
        {
            "$match": {
                "brand_id": brand_id,
                "timestamp": {"$gte": start_date}
            }
        },
        {
            "$project": {
                "hour": {"$hour": "$timestamp"}
            }
        },
        {
            "$group": {
                "_id": "$hour",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    
    results = list(drink_clicks.aggregate(pipeline))
    
    # 初始化 24 小時
    hourly_dist = {h: 0 for h in range(24)}
    
    # 填入數據
    for r in results:
        hourly_dist[r["_id"]] = r["count"]
    
    return hourly_dist


def clean_old_records(days=90):
    """清理 N 天前的舊記錄（定期維護用）
    
    Args:
        days: 保留最近幾天的資料
    
    Returns:
        int: 刪除的記錄數
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    result = drink_clicks.delete_many({
        "timestamp": {"$lt": cutoff_date}
    })
    
    return result.deleted_count
