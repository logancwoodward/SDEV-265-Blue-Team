import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to load responses from the JSON file
def load_responses():
    with open('data/responses.json') as f:
        return json.load(f)

responses = load_responses()  # Load the responses from the JSON file

# Route to render the main page with the chatbot
@app.route('/')
def index():
    return render_template('index.html')

# API route for the chatbot to process the user input
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input').lower()  # Convert input to lowercase for easier matching
    
    # Check if the user input matches a key in the responses
    for key, value in responses.items():
        if key.lower() in user_input:  # Match the user's input to a response
            return jsonify({'response': value})

    # If no match is found, return the default response
    return jsonify({'response': responses.get('default', 'Sorry, I don\'t understand that. Can you ask something else?')})

if __name__ == '__main__':
    app.run(debug=True)

