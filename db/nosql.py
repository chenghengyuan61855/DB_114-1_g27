from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
nosql_db = client["nosql_database"]

drink_clicks = nosql_db["drink_clicks"]
