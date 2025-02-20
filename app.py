from flask import Flask, render_template, request, jsonify, redirect, session
from database.database_manager import DatabaseManager, ResponseManager, AdminManager
from tools.keyword_extractor import extract_keywords
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")  # Uses env variable for Render, fallback locally

# Initialize database and managers
db = DatabaseManager()
response_manager = ResponseManager(db)
admin_manager = AdminManager(db)


@app.route("/")
def index():
    """Renders the chatbot UI."""
    return render_template("index.html")

### 🔒 ADMIN AUTHENTICATION ROUTES ###
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    """Handles admin login authentication."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if admin_manager.verify_admin(username, password):
            session["admin"] = username  # Store admin session
            return redirect("/admin_dashboard")
        else:
            return "Invalid credentials", 401

    return render_template("admin_login.html")  # Login page

@app.route("/admin_dashboard")
def admin_dashboard():
    """Admin Panel after login."""
    if "admin" not in session:
        return redirect("/admin")
    return render_template("admin.html", admin=session["admin"])

@app.route("/logout")
def logout():
    """Logs out the admin."""
    session.pop("admin", None)
    return redirect("/admin")

### 🔍 ADMIN RESPONSE MANAGEMENT ROUTES ###
@app.route("/get_responses", methods=["GET"])
def get_responses():
    """Fetch responses for admin panel with pagination."""
    if "admin" not in session:
        return redirect("/admin")

    page = int(request.args.get("page", 1))
    return jsonify(response_manager.get_responses(page=page))

@app.route("/add_response", methods=["POST"])
def add_response():
    """Add a chatbot response (restricted to admin)."""
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    return jsonify(response_manager.add_response(data.get("keyword"), data.get("response"), data.get("link")))

@app.route("/edit_response", methods=["POST"])
def edit_response():
    """Edit an existing chatbot response (restricted to admin)."""
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    return jsonify(response_manager.edit_response(data.get("keyword"), data.get("response"), data.get("link")))

@app.route("/delete_response", methods=["POST"])
def delete_response():
    """Delete a chatbot response (restricted to admin)."""
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    return jsonify(response_manager.delete_response(data.get("keyword")))

### 💬 CHATBOT RESPONSE ROUTE ###
@app.route("/get_response", methods=["POST"])
def get_response():
    """Handles chatbot response requests."""
    data = request.json
    user_message = data.get("message", "").lower()

    keywords = extract_keywords(user_message)

    for keyword in keywords:
        print(keyword)
        response_text = response_manager.get_response(keyword)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
