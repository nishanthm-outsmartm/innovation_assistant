# init_db.py
from app import app
from models import db

with app.app_context():
    db.create_all()  # This will create all the tables in the database
