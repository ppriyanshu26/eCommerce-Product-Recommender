# 🛍️ AI-Powered E-Commerce Product Recommender

A modern, intelligent product recommendation system that leverages machine learning and AI to provide personalized shopping experiences. The system analyzes user behavior (views, cart additions, purchases) and uses TF-IDF-based content filtering combined with OpenAI's GPT to generate contextual, human-friendly explanations for each recommendation.

## ✨ Key Features

- 🎯 **Personalized Recommendations** - ML-powered product suggestions based on individual user behavior
- 🤖 **AI-Generated Explanations** - Natural language insights explaining why products are recommended
- 📊 **Behavioral Tracking** - Real-time monitoring of user interactions (views, cart additions, purchases)
- ⚡ **Smart Ranking Algorithm** - Weighted scoring system (viewed: 1x, cart: 2x, purchased: 3x)
- 🔍 **Content-Based Filtering** - TF-IDF vectorization for intelligent product similarity matching
- 💬 **Contextual Understanding** - GPT-4 integration for human-friendly recommendation narratives
- 🎨 **Modern UI/UX** - Clean, responsive design with glassmorphism effects
- 📱 **RESTful API** - Well-structured endpoints for seamless frontend-backend communication
- 🔐 **Secure Configuration** - Environment-based secrets management
- 🗄️ **Scalable Database** - MongoDB Atlas for flexible, cloud-based data storage

## 🚀 Tech Stack

### **Backend** 🐍
- **Flask** - Lightweight Python web framework for building RESTful APIs
- **MongoDB** - NoSQL database for flexible storage of users, products, and behavioral data
- **PyMongo** - Official MongoDB driver for seamless Python integration
- **OpenAI API** - GPT-4 integration for generating natural language recommendation explanations
- **scikit-learn** - Machine learning library for TF-IDF vectorization and cosine similarity calculations
- **NumPy** - Numerical computing for efficient vector operations in the recommendation engine

### **Frontend** ⚛️
- **React** - Component-based UI library for building an interactive user interface
- **Axios** - Promise-based HTTP client for API communication with the backend
- **CSS3** - Modern styling with gradients, glassmorphism effects, and responsive design
- **Google Fonts (Inter)** - Clean, professional typography

### **DevOps & Tools** 🛠️
- **python-dotenv** - Environment variable management for secure configuration
- **Flask-CORS** - Cross-Origin Resource Sharing support for frontend-backend communication
- **React Scripts** - Build tooling and development server for the React application

## 🔄 System Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    User Interaction Captured
          (Product View / Add to Cart / Purchase)
                              │
                              ▼
                    ┌─────────────────────┐
                    │   Axios HTTP POST   │
                    │   /track-behavior   │
                    └─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (Flask API)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Receive User Behavior Data
                    (user_id, product_id, action)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE (MongoDB)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
  Store Behavior              Query User History & Products
  (views, cart, purchase)     (behaviors + product metadata)
        │                                           │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RECOMMENDATION ENGINE                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              TF-IDF Vectorization (scikit-learn)
              Product Descriptions → Feature Vectors
                              │
                              ▼
              Cosine Similarity Calculation (NumPy)
              Find Top Similar Products
                              │
                              ▼
              Apply Behavioral Weights
              (viewed: 1x, cart: 2x, purchased: 3x)
                              │
                              ▼
              Generate Top N Recommendations
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OPENAI API (GPT-4)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        Send Recommended Products + User Context
                              │
                              ▼
        Generate Natural Language Explanations
        "Based on your interest in..."
                              │
                              ▼
        Return AI-Enhanced Recommendations
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (Flask API)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              Format JSON Response
              (products + AI explanations)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              Display Personalized Recommendations
              with AI-Generated Insights
                              │
                              ▼
                      ✨ User Sees Results ✨
```

### **Step-by-Step Process** 📋

1. **User Action** 👤 - User interacts with products (view, add to cart, purchase)
2. **Data Capture** 📡 - React frontend captures the interaction and sends it via Axios
3. **API Endpoint** 🔌 - Flask receives the data at `/track-behavior` endpoint
4. **Database Storage** 💾 - User behavior is stored in MongoDB for future analysis
5. **Data Retrieval** 🔍 - Backend queries user history and product catalog from MongoDB
6. **ML Processing** 🤖 - TF-IDF vectorization and cosine similarity calculate product similarities
7. **Weighted Ranking** ⚖️ - Behaviors are weighted (view < cart < purchase) for better recommendations
8. **AI Enhancement** ✨ - Top recommendations sent to OpenAI GPT-4 for contextual explanations
9. **Response Formation** 📦 - Combined product data + AI insights packaged as JSON
10. **Frontend Display** 🎨 - React renders personalized recommendations with explanations

## 📥 Installation & Setup

### **Prerequisites** 📋
- Python 3.8 or higher
- Node.js 16 or higher
- MongoDB Atlas account (or MongoDB installed locally)
- OpenAI API Key

### **Step 1: Clone the Repository** 📂
```bash
git clone https://github.com/ppriyanshu26/eCommerce-Product-Recommender.git
cd eCommerce-Product-Recommender
```

### **Step 2: Backend Setup** 🔧

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment
```bash
python -m venv venv
```

#### Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Install Backend Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
Create a `.env` file in the **root directory** (not in backend folder):
```bash
MONGO_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
OPENAI_API_KEY=your_openai_api_key_here
API_URL=http://127.0.0.1:5000
```

💡 **Note:** Replace with your actual MongoDB Atlas connection string and OpenAI API key.

#### Update Seed Data (Optional)
Edit `data.json` to customize your product catalog with your own products, descriptions, and pricing.

#### Seed the Database
```bash
python data.py
```
✅ This will populate MongoDB with users, products, and sample behaviors.

#### Start the Backend Server
```bash
python app.py
```
🚀 Backend will be running on **http://localhost:5000**

---

### **Step 3: Frontend Setup** 🎨

Open a **new terminal** and navigate to the frontend directory:

```bash
cd frontend
```

#### Install Frontend Dependencies
```bash
npm install
```

#### Start the React Development Server
```bash
npm start
```

🎉 Frontend will automatically open in your browser at **http://localhost:3000**

---

## 🌐 Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **Database:** MongoDB Atlas Cloud

---

## ⚠️ Common Issues & Troubleshooting

<details>
<summary><b>1. MongoDB Connection Errors 🔴</b></summary>

<br>

**Error:** `pymongo.errors.ServerSelectionTimeoutError` or `connection refused`

**Solutions:**
- ✅ Verify your MongoDB Atlas connection string in `.env`
- ✅ Check if your IP address is whitelisted in MongoDB Atlas (Network Access)
- ✅ Ensure database user credentials are correct
- ✅ Confirm `retryWrites=true&w=majority` parameters are in the connection string

```bash
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
```

</details>

---

<details>
<summary><b>2. OpenAI API Key Issues 🔑</b></summary>

<br>

**Error:** `openai.error.AuthenticationError` or `Invalid API Key`

**Solutions:**
- ✅ Verify your OpenAI API key is valid and active
- ✅ Check for extra spaces or quotes in the `.env` file
- ✅ Ensure you have sufficient API credits
- ✅ Regenerate API key from OpenAI dashboard if needed

</details>

---

<details>
<summary><b>3. CORS Errors 🚫</b></summary>

<br>

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solutions:**
- ✅ Ensure `flask-cors` is installed: `pip install flask-cors`
- ✅ Verify `CORS(app)` is present in `app.py`
- ✅ Check that backend is running on port 5000
- ✅ Confirm frontend is making requests to `http://localhost:5000`

</details>

---

<details>
<summary><b>4. Port Already in Use 🔌</b></summary>

<br>

**Error:** `OSError: [Errno 48] Address already in use` or `Port 5000/3000 is already in use`

**Solutions:**

**For Backend (Port 5000):**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**For Frontend (Port 3000):**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <process_id> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

</details>

---

<details>
<summary><b>5. Module Not Found Errors 📦</b></summary>

<br>

**Error:** `ModuleNotFoundError: No module named 'flask'` or similar

**Solutions:**
- ✅ Ensure virtual environment is activated (`venv\Scripts\activate`)
- ✅ Reinstall dependencies: `pip install -r requirements.txt`
- ✅ Check Python version: `python --version` (should be 3.8+)
- ✅ For frontend: Delete `node_modules` and run `npm install` again

</details>

---

<details>
<summary><b>6. Empty Recommendations 📭</b></summary>

<br>

**Error:** No recommendations displayed or empty array returned

**Solutions:**
- ✅ Verify database was seeded: `python data.py`
- ✅ Check MongoDB contains users, products, and behaviors collections
- ✅ Ensure user_id exists in the database
- ✅ Try with different user_ids (e.g., user_1, user_2, user_3)

</details>

---

<details>
<summary><b>7. Environment Variables Not Loading 🌍</b></summary>

<br>

**Error:** `KeyError: 'MONGO_URI'` or OpenAI API not working

**Solutions:**
- ✅ Confirm `.env` file is in the **root directory** (not in backend folder)
- ✅ Check file is named `.env` (not `.env.txt`)
- ✅ Restart the Flask server after modifying `.env`
- ✅ Verify `load_dotenv()` is called in `app.py`

</details>

---

<details>
<summary><b>8. React App Not Starting ⚛️</b></summary>

<br>

**Error:** `npm start` fails or dependency issues

**Solutions:**
- ✅ Delete `node_modules` and `package-lock.json`
- ✅ Run `npm install` again
- ✅ Clear npm cache: `npm cache clean --force`
- ✅ Check Node.js version: `node --version` (should be 16+)
- ✅ Try `npm install --legacy-peer-deps` if dependency conflicts occur

</details>

---

<details>
<summary><b>9. Data Seeding Failures 🌱</b></summary>

<br>

**Error:** `python data.py` fails or data not inserted

**Solutions:**
- ✅ Check MongoDB connection is working
- ✅ Verify `data.json` is properly formatted (valid JSON)
- ✅ Ensure collections don't already exist (drop them if needed)
- ✅ Check MongoDB user has write permissions

</details>

---

<details>
<summary><b>10. OpenAI Rate Limit Exceeded ⏱️</b></summary>

<br>

**Error:** `openai.error.RateLimitError: You exceeded your current quota`

**Solutions:**
- ✅ Check your OpenAI usage limits and billing
- ✅ Reduce the number of recommendation requests
- ✅ Implement caching for frequently requested recommendations
- ✅ Consider upgrading your OpenAI plan

</details>

---

### **Need More Help?** 🆘

If you encounter issues not listed here:

1. Check the terminal/console for detailed error messages
2. Verify all prerequisites are installed and up-to-date
3. Ensure `.env` variables are correctly configured
4. Review the Flask and React logs for specific errors
5. Try running with debug mode: `flask run --debug`

---

## 🤝 Contributing

We welcome contributions to improve the AI-Powered E-Commerce Product Recommender! Follow these steps to contribute:

### **Step 1: Fork the Repository** 🍴

Click the **Fork** button at the top right of this repository to create your own copy.

---

### **Step 2: Clone Your Fork** 📥

```bash
git clone https://github.com/your-username/eCommerce-Product-Recommender.git
cd eCommerce-Product-Recommender
```

---

### **Step 3: Create a New Branch** 🌿

Create a branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
```

---

### **Step 4: Make Your Changes** ✏️

Make your changes to the codebase.

---

### **Step 5: Commit Your Changes** 💾

Stage and commit your changes with a descriptive message:

```bash
git add .
git commit -m "Add: Brief description of your changes"
```

---

### **Step 6: Push to Your Fork** 🚀

Push your changes to your forked repository:

```bash
git push origin feature/your-feature-name
```

---

### **Step 7: Open a Pull Request** 📬

1. Go to the original repository on GitHub
2. Click the **"Pull Request"** button
3. Click **"New Pull Request"**
4. Select your fork and branch
5. Fill in the PR template with:
6. Click **"Create Pull Request"**

---

### **Questions or Suggestions?** 💬

Feel free to:
- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Contact the maintainers directly

**Thank you for contributing!** 🙏

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [Priyanshu Priyam](https://github.com/ppriyanshu26)
- LinkedIn: [Priyanshu Priyam](https://linkedin.com/in/ppriyanshu26)
- Email: contact@ppriyanshu26.online

---

## 🌟 Acknowledgments

- OpenAI for providing the GPT API
- MongoDB Atlas for cloud database hosting
- The open-source community for amazing tools and libraries

---

<div align="center">

**Made with ❤️ and ☕**

⭐ **Star this repo if you found it helpful!** ⭐

</div>