from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("ecommerce")

def get_products(product_ids=None):
    products_collection = db.get_collection("products")
    if product_ids:
        from bson.objectid import ObjectId
        product_ids = [ObjectId(pid) for pid in product_ids]
        return list(products_collection.find({"_id": {"$in": product_ids}}))
    return list(products_collection.find({}))

def get_user_behavior(user_id):
    behavior_collection = db.get_collection("user_behavior")
    return list(behavior_collection.find({"user_id": user_id}))

def get_all_users():
    users_collection = db.get_collection("users")
    # Return only user_id and name
    return list(users_collection.find({}, {"user_id": 1, "name": 1, "_id": 0}))
