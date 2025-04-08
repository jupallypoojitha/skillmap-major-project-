from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os
import traceback
from markdown import markdown

# Load environment variables
load_dotenv()

# Set up Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure Google Gemini AI
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API key is missing. Set GEMINI_API_KEY as an environment variable.")

print("API Key Loaded: " + "*" * len(API_KEY))  # Mask API key for security

genai.configure(api_key=API_KEY)

# Serve SkillMap homepage
@app.route("/")
def serve_index():
    return send_from_directory(os.path.abspath("../mainfiles"), "skillmap.html")

# Search API endpoint
@app.route("/api/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"response": "Please enter a valid search term."}), 400

        # Structured prompt for better output
        enhanced_query = f"""
You are an AI assistant specializing in **structured learning roadmaps** and **study resources**.

## 📌 User's Question: {query}

### 🎯 **Roadmap Overview for Mastering {query}**
#### 🔹 Beginner Stage:
- First steps and foundational knowledge
- Key concepts to understand  

#### 🔹 Intermediate Stage:
- Hands-on projects  
- Deeper concepts and practical applications  

#### 🔹 Advanced Stage:
- Expert-level learning  
- Specialized skills and career applications  

---

### 📚 **Recommended Resources**
#### 📖 **Top 3 Books:**
1. **Book Title 1** - Author Name  
2. **Book Title 2** - Author Name  
3. **Book Title 3** - Author Name  

#### 🎓 **Essential Courses:**
1. **Course Name 1** - Platform (e.g., Coursera, Udemy)  
2. **Course Name 2** - Platform  

#### 🔗 **Helpful Websites:**
1. [Website Name 1](URL)  
2. [Website Name 2](URL)  

#### 🎥 **Videos & Podcasts:**
- [Video Title](URL) - **YouTube/TED/Podcast Name**  
- [Podcast Title](URL) - **Podcast Platform**  

---

### 🕒 **Timeframe & Learning Path**
- **Beginner Stage**: X weeks  
- **Intermediate Stage**: X weeks  
- **Advanced Stage**: X weeks  

### ✅ **Focus on:**
- **Concise & Actionable Steps**
- **Avoid unnecessary explanations**
- **Structured learning with the best resources**
"""

        model = genai.GenerativeModel("gemini-1.5-flash")  # Use "pro" for better quality
        response = model.generate_content(enhanced_query)

        # Ensure valid response
        response_text = response.text if hasattr(response, 'text') else str(response)

        # Convert Markdown to formatted HTML for better readability
        formatted_response = markdown(response_text)

        return jsonify({"response": formatted_response})

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"An error occurred:\n{error_details}")  # Logs full stack trace
        return jsonify({"response": "An internal error occurred."}), 500

# Run Flask app dynamically on available port
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use dynamic port
    app.run(debug=True, host='0.0.0.0', port=port)


app = Flask(__name__)

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)