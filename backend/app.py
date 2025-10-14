from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import get_recommendations
from db import get_products, get_user_behavior, get_all_users
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🛍️ AI-Powered E-Commerce Recommender API",
        "status": "running",
        "endpoints": {
            "users": "/users",
            "recommendations": "/recommendations?user_id=<user_id>",
            "user_behavior": "/user_behavior?user_id=<user_id>"
        }
    })

@app.route('/users', methods=['GET'])
def users():
    users = get_all_users()
    return jsonify(users)

@app.route('/recommendations', methods=['GET'])
def recommendations():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    recommendations = get_recommendations(user_id)
    return jsonify(recommendations)

@app.route('/user_behavior', methods=['GET'])
def user_behavior():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
        
    behavior = get_user_behavior(user_id)
    
    # Get product details for the product_ids
    product_ids = [item['product_id'] for item in behavior]
    products = get_products(product_ids)
    
    product_map = {product['_id']: product for product in products}
    
    enriched_behavior = {
        "viewed": [],
        "added_to_cart": [],
        "purchased": []
    }
    
    for item in behavior:
        product_info = product_map.get(item['product_id'])
        if product_info:
            if item['interaction_type'] == 'viewed':
                enriched_behavior['viewed'].append(product_info)
            elif item['interaction_type'] == 'added_to_cart':
                enriched_behavior['added_to_cart'].append(product_info)
            elif item['interaction_type'] == 'purchased':
                enriched_behavior['purchased'].append(product_info)

    # Limit to recent 3 for each category
    enriched_behavior['viewed'] = enriched_behavior['viewed'][-3:]
    enriched_behavior['added_to_cart'] = enriched_behavior['added_to_cart'][-3:]
    enriched_behavior['purchased'] = enriched_behavior['purchased'][-3:]

    # Convert ObjectId to string for JSON serialization
    for category in enriched_behavior.values():
        for product in category:
            product['_id'] = str(product['_id'])

    return jsonify(enriched_behavior)


if __name__ == '__main__':
    app.run(debug=True)