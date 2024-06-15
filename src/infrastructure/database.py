from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["barter_app"]

users_collection = db["users"]
products_collection = db["products"]
offers_collection = db["offers"]