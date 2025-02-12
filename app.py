from flask import Flask, render_template, request, jsonify
from tools.web_scraper import extract_keywords
import sqlite3


app = Flask(__name__)

# Path to the database file
DB_PATH = "database/chatbot.db"

# Function to get a response from the database
def get_response_from_db(keyword):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT response, link FROM responses WHERE keyword LIKE ?", ('%' + keyword + '%',))
    result = cursor.fetchone()
    connection.close()
    return result

# Route to render the chatbot page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle user inputs and send responses
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    keywords = extract_keywords(user_input)
    if len(keywords) > 1:
        for keyword in keywords:
            result = get_response_from_db(keyword)
    if len(keywords) == 1:
        result = get_response_from_db(keyword)
    print(result)

    if result:
        response, link = result
        if link:
            response += f' <a href="{link}" target="_blank">Learn more</a>'
        return jsonify({'response': response})
    else:
        if len(keywords) == 0:
            return jsonify({'response': 'Oops! It appears that you didn\'t enter anything. Be sure to type out your request before hitting enter.'})
        return jsonify({'response': "Sorry, I don't understand that. Can you ask something else?"})




# Route to render the admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Route to add responses via the admin panel
@app.route('/add_response', methods=['POST'])
def add_response():
    keyword = request.form['keyword']
    response = request.form['response']
    link = request.form.get('link')  # Optional field

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO responses (keyword, response, link) VALUES (?, ?, ?)", 
                   (keyword, response, link))
    connection.commit()
    connection.close()

    
    # Full HTML structure for success message
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Response Added</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <div class="success-message">
            <p>Response added successfully!</p>
            <a href='/admin'>Go back to Admin Panel</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
