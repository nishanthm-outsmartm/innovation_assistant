from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database
db = SQLAlchemy()

# Idea model for storing generated innovation ideas
class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(500), nullable=False)  # Store the user prompt
    idea = db.Column(db.Text, nullable=False)           # Store the generated idea
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of idea creation

    def __repr__(self):
        return f'<Idea {self.id} - {self.idea[:50]}>'
