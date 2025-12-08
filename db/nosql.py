from pymongo import MongoClient

# 設定較短的超時時間，避免連線失敗時等待過久
client = MongoClient(
    "mongodb://localhost:27017",
    serverSelectionTimeoutMS=2000,  # 2秒超時
    connectTimeoutMS=2000,
    socketTimeoutMS=2000
)
nosql_db = client["nosql_database"]

drink_clicks = nosql_db["drink_clicks"]
