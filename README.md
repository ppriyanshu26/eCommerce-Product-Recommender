# E-commerce Product Recommender

This project is a simple e-commerce product recommender that uses a combination of collaborative filtering and a Large Language Model (LLM) to provide personalized product recommendations with explanations.

## Project Structure

```
.
├── backend
│   ├── app.py              # Flask application
│   ├── db.py               # Database connection and queries
│   ├── recommender.py      # Recommendation logic
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Example environment variables
└── frontend
    ├── index.html          # Main HTML file
    ├── script.js           # JavaScript for API calls and DOM manipulation
    └── style.css           # CSS for styling
```

## How to Set Up and Run

### 1. Backend

1.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    *   Rename `.env.example` to `.env`.
    *   Open the `.env` file and add your MongoDB Atlas connection string and your OpenAI API key.
        ```
        MONGO_URI=your_mongodb_atlas_connection_string
        OPENAI_API_KEY=your_openai_api_key
        ```

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The backend server will start on `http://127.0.0.1:5000`.

### 2. Database Setup (MongoDB Atlas)

You need to create a database (e.g., `ecommerce`) with three collections: `users`, `products`, and `user_behavior`.

Here is some sample data you can insert into your collections:

**`users` collection:**
```json
[
  {
    "user_id": "user1",
    "name": "Alice"
  },
  {
    "user_id": "user2",
    "name": "Bob"
  }
]
```

**`products` collection:**
```json
[
  {
    "name": "Laptop",
    "category": "Electronics",
    "description": "A high-performance laptop for all your needs."
  },
  {
    "name": "Smartphone",
    "category": "Electronics",
    "description": "A smartphone with a great camera."
  },
  {
    "name": "Headphones",
    "category": "Electronics",
    "description": "Noise-cancelling headphones for an immersive audio experience."
  },
  {
    "name": "Coffee Maker",
    "category": "Home Appliances",
    "description": "Brews the perfect cup of coffee every morning."
  },
  {
    "name": "Blender",
    "category": "Home Appliances",
    "description": "A powerful blender for smoothies and more."
  }
]
```

**`user_behavior` collection:**

*Make sure to replace `"product_id_x"` with the actual `_id` values of the products you inserted in the `products` collection.*

```json
[
  { "user_id": "user1", "product_id": "<product_id_laptop>", "interaction_type": "purchased" },
  { "user_id": "user1", "product_id": "<product_id_headphones>", "interaction_type": "added_to_cart" },
  { "user_id": "user1", "product_id": "<product_id_smartphone>", "interaction_type": "viewed" },
  { "user_id": "user2", "product_id": "<product_id_coffee_maker>", "interaction_type": "purchased" },
  { "user_id": "user2", "product_id": "<product_id_blender>", "interaction_type": "viewed" }
]
```

### 3. Frontend

1.  Open the `frontend/index.html` file in your web browser.
2.  Select a user from the dropdown to see their recent activity and personalized recommendations.

## How It Works

1.  **User Selection**: The frontend fetches the list of users from the `/users` endpoint and populates a dropdown.
2.  **Data Fetching**: When a user is selected, the frontend makes two API calls:
    *   `GET /user_behavior?user_id=<selected_user>`: To get the user's recent activity.
    *   `GET /recommendations?user_id=<selected_user>`: To get product recommendations.
3.  **Recommendation Logic**:
    *   The backend calculates a "user profile" based on the weights of their interactions (`viewed`, `added_to_cart`, `purchased`).
    *   It uses TF-IDF to create vector representations of the products based on their name, category, and description.
    *   It computes a weighted average of the vectors of the products the user has interacted with to create a "user interest" vector.
    *   It then calculates the cosine similarity between the user interest vector and all product vectors to find the most similar products.
4.  **LLM Explanation**:
    *   For each recommended product, the backend sends a prompt to the OpenAI API asking it to explain why the product is a good recommendation based on the user's behavior.
5.  **Display**: The frontend displays the user's activity and the recommended products with their explanations in a simple dashboard format.
