from flask import Flask, render_template, request
import requests  # For making HTTP requests to the API
from models import db, Idea  # Import the database and Idea model

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Set your Groq API key
GROQ_API_KEY = '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'  # Replace with your Groq API key
API_URL = "https://api.groq.com/your-model-endpoint"  # Replace with your Groq model URL

# Route to home page
@app.route('/')
def index():
    ideas = Idea.query.all()  # Fetch all ideas from the database
    return render_template('index.html', ideas=ideas)

# Route to generate and display ideas
@app.route('/generate_idea', methods=['POST'])
def generate_idea():
    prompt = request.form.get('prompt')
    
    # Prepare the payload to send to the Groq API
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }

    # The payload contains the prompt that will be sent to the model
    payload = {
        "input": prompt,  # Adjust according to Groq's API documentation
    }

    # Send the POST request to the Groq API    
    # Check if the request was successful
# Send the POST request to the API and check response status
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            idea_text = response.json()['generated_output'].strip()  # Adjust if response format is different
        except KeyError:
            idea_text = "Error: Missing expected response key."
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")  # Log full response for debugging
        idea_text = "Error: Could not generate idea. Please try again later."

    # Store the idea in the database
    new_idea = Idea(prompt=prompt, idea=idea_text)
    db.session.add(new_idea)
    db.session.commit()  # Commit the change to the database

    return render_template('result.html', idea=idea_text)

if __name__ == '__main__':
    app.run(debug=True)
