import openai
from db import get_products, get_user_behavior
import os
from dotenv import load_dotenv, find_dotenv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv(find_dotenv())

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_recommendations(user_id):
    user_behavior = get_user_behavior(user_id)
    all_products = get_products()

    if not user_behavior:
        # If no user behavior, recommend top 3 most popular products (e.g., by sales or views)
        # For simplicity, returning first 3 products
        return all_products[:3]

    # Create a profile of the user based on their behavior
    user_profile = {}
    weights = {"viewed": 1, "added_to_cart": 2, "purchased": 3}

    for item in user_behavior:
        product_id = item["product_id"]
        interaction_type = item["interaction_type"]
        
        if product_id not in user_profile:
            user_profile[product_id] = 0
        user_profile[product_id] += weights[interaction_type]

    # Get product details for the products the user has interacted with
    interacted_product_ids = list(user_profile.keys())
    interacted_products = get_products(interacted_product_ids)
    
    if not interacted_products:
        return all_products[:3]

    # Combine product attributes for TF-IDF
    product_docs = [f"{p['name']} {p['category']} {p['description']}" for p in all_products]
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(product_docs)

    # Calculate user's interest vector
    user_vector = np.zeros(tfidf_matrix.shape[1])
    
    product_id_to_index = {str(p['_id']): i for i, p in enumerate(all_products)}

    for product in interacted_products:
        product_id_str = str(product['_id'])
        if product_id_str in product_id_to_index:
            idx = product_id_to_index[product_id_str]
            # Weight the product's vector by the user's interaction score
            user_vector += user_profile[product['_id']] * tfidf_matrix[idx]

    user_vector = user_vector.reshape(1, -1)

    # Calculate similarity between user vector and all product vectors
    cosine_similarities = cosine_similarity(np.asarray(user_vector), tfidf_matrix)
    
    # Get IDs of products user has already interacted with to filter them out
    interacted_product_ids_str = {str(pid) for pid in user_profile.keys()}
    
    # Get top 10 potential recommendations (to increase variety)
    similar_indices = cosine_similarities[0].argsort()[-13:][::-1]
    
    recommendations = []
    for i in similar_indices:
        if len(recommendations) >= 3:
            break  # Stop when we have 3 recommendations
            
        product = all_products[i]
        product_id_str = str(product['_id'])
        
        # Skip if user has already interacted with this product
        if product_id_str in interacted_product_ids_str:
            continue
            
        # Convert ObjectId to string for JSON serialization
        product['_id'] = product_id_str
        explanation = generate_explanation(product, user_behavior)
        recommendations.append({
            "product": product,
            "explanation": explanation
        })

    return recommendations

def generate_explanation(product, user_behavior):
    # Build a summary of user behavior
    behavior_summary = []
    
    # Get details of products user interacted with
    interacted_product_ids = [item['product_id'] for item in user_behavior]
    interacted_products = get_products(interacted_product_ids)
    product_map = {str(p['_id']): p for p in interacted_products}

    for item in user_behavior:
        p_info = product_map.get(str(item['product_id']))
        if p_info:
            behavior_summary.append(f"{item['interaction_type']} {p_info['name']} ({p_info['category']})")
    
    behavior_text = ", ".join(behavior_summary[:5])  # Limit to 5 most recent items
    
    prompt = (
        f"You are an e-commerce recommendation assistant. A user has recently interacted with these products: {behavior_text}. "
        f"We are now recommending '{product['name']}' from the {product['category']} category. "
        f"Product description: {product['description']}. "
        f"In one friendly sentence, explain why this is a good recommendation for them."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful e-commerce recommendation assistant. Provide concise, friendly explanations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.4
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return "This product is recommended for you based on your recent activity."
