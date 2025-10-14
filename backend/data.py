import json
import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_seed_data():
    """Loads seed data configuration from JSON file."""
    json_path = os.path.join(os.path.dirname(__file__), "seed_data.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: seed_data.json not found at {json_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in seed_data.json: {e}")
        return None

def generate_data():
    """Generates sample data for users, products, and interactions from JSON config."""
    
    seed_config = load_seed_data()
    if not seed_config:
        return {"users": [], "products": [], "user_behavior": []}
    
    # --- User Data ---
    users = seed_config.get("users", [])

    # --- Product Data ---
    product_config = seed_config.get("product_config", {})
    adjectives = product_config.get("adjectives", [])
    product_types = product_config.get("product_types", [])
    categories = product_config.get("categories", {})
    features = product_config.get("features", [])
    num_products = product_config.get("num_products", 50)
    
    # Start with custom products if any
    products = seed_config.get("custom_products", []).copy()
    product_names = {p["name"] for p in products}
    
    # Generate additional products
    for i in range(num_products - len(products)):
        if not adjectives or not product_types:
            break
            
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
        
        feature = random.choice(features) if features else "premium quality"
        products.append({
            "name": name,
            "category": category,
            "description": f"A top-quality {name} for all your needs. Features include {feature}."
        })

    # --- User Behavior Data ---
    interaction_config = seed_config.get("interaction_config", {})
    interaction_types = interaction_config.get("interaction_types", ["viewed", "added_to_cart", "purchased"])
    interaction_weights = interaction_config.get("interaction_weights", [0.6, 0.3, 0.1])
    min_interactions = interaction_config.get("min_interactions_per_user", 5)
    max_interactions = interaction_config.get("max_interactions_per_user", 15)
    
    user_behavior = []
    for user in users:
        # Each user interacts with a random number of products
        num_interactions = random.randint(min_interactions, max_interactions)
        for _ in range(num_interactions):
            if not products:
                break
            product = random.choice(products)
            interaction = random.choices(interaction_types, weights=interaction_weights, k=1)[0]
            
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
