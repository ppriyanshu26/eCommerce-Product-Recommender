import json
import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_data():
    """Generates sample data for users, products, and interactions."""
    
    # --- User Data ---
    users = [
        {"user_id": "user1", "name": "Alice"},
        {"user_id": "user2", "name": "Bob"},
        {"user_id": "user3", "name": "Charlie"}
    ]

    # --- Product Data ---
    adjectives = ["High-Performance", "Sleek", "Durable", "Lightweight", "Ergonomic", "Smart", "Wireless", "Premium", "Eco-Friendly", "Compact"]
    product_types = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "Charger", "Speaker", "Tablet", "Stylus", "Coffee Maker", "Blender", "Toaster", "Book", "T-Shirt", "Yoga Mat"]
    categories = {
        "Electronics": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "Charger", "Speaker", "Tablet", "Stylus"],
        "Home Appliances": ["Coffee Maker", "Blender", "Toaster"],
        "Books": ["Book"],
        "Apparel": ["T-Shirt"],
        "Health & Wellness": ["Yoga Mat"]
    }

    products = []
    product_names = set()
    for i in range(50):
        adj = random.choice(adjectives)
        ptype = random.choice(product_types)
        name = f"{adj} {ptype}"
        
        # Ensure unique product names
        if name in product_names:
            name = f"{name} {i+1}"
        product_names.add(name)

        category = "Miscellaneous"
        for cat, types in categories.items():
            if ptype in types:
                category = cat
                break
        
        products.append({
            "name": name,
            "category": category,
            "description": f"A top-quality {name} for all your needs. Features include {random.choice(['long battery life', 'fast charging', 'high resolution', 'ergonomic design'])}."
        })

    # --- User Behavior Data ---
    interactions = ["viewed", "added_to_cart", "purchased"]
    user_behavior = []
    for user in users:
        # Each user interacts with 5 to 15 products
        for _ in range(random.randint(5, 15)):
            product = random.choice(products)
            interaction = random.choices(interactions, weights=[0.6, 0.3, 0.1], k=1)[0]
            
            # Find the product's placeholder ID for the behavior record
            product_name = product["name"]

            user_behavior.append({
                "user_id": user["user_id"],
                "product_name": product_name, # We'll use this to find the real _id later
                "interaction_type": interaction
            })
            
    return {"users": users, "products": products, "user_behavior": user_behavior}


def seed_database():
    """Seeds the MongoDB database with sample data."""
    
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        print("MONGO_URI not found in .env file. Please add it.")
        return

    try:
        client = MongoClient(MONGO_URI)
        db = client.get_database("ecommerce")
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    data = generate_data()

    # Clear existing collections
    db.users.delete_many({})
    db.products.delete_many({})
    db.user_behavior.delete_many({})
    print("Cleared existing data in collections.")

    # Insert users
    db.users.insert_many(data["users"])
    print(f"Inserted {len(data['users'])} users.")

    # Insert products and get their new _ids
    product_result = db.products.insert_many(data["products"])
    print(f"Inserted {len(product_result.inserted_ids)} products.")
    
    # Create a map of product name to its new _id
    inserted_products = list(db.products.find({}))
    product_name_to_id = {p['name']: p['_id'] for p in inserted_products}

    # Prepare and insert user behavior with correct product_id
    behavior_to_insert = []
    for behavior in data["user_behavior"]:
        product_id = product_name_to_id.get(behavior["product_name"])
        if product_id:
            behavior_to_insert.append({
                "user_id": behavior["user_id"],
                "product_id": product_id,
                "interaction_type": behavior["interaction_type"]
            })
    
    if behavior_to_insert:
        db.user_behavior.insert_many(behavior_to_insert)
        print(f"Inserted {len(behavior_to_insert)} user behavior records.")

    client.close()
    print("Database seeding complete. Connection closed.")


if __name__ == "__main__":
    # This allows running the script directly to seed the database
    # Example: python data.py
    seed_database()
