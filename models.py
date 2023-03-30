"""Models for Adopt."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://w7.pngwing.com/pngs/648/971/png-transparent-dog-cat-puppy-animal-rescue-group-animal-shelter-dog-horse-white-animals-thumbnail.png"

class Pet(db.Model):
    
    __tablename__ = "pets"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text, default=DEFAULT_IMG_URL)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)
    
def connect_db(app):
    """Connect this database to Flask app"""
    db.app = app
    db.init_app(app)