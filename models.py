from app import db, login_manager  # Import from our app instance
from flask_login import UserMixin  # Provides default implementations for Flask-Login
from datetime import datetime  # For timestamping user creation

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Query the User table by ID
    return User.query.get(int(user_id))

# User model definition
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(50), unique=True, nullable=False)  # User's unique name
    email = db.Column(db.String(100), unique=True, nullable=False)  # User's unique email
    password = db.Column(db.String(60), nullable=False)  # Hashed password
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for user creation

    def __repr__(self):
        # Representation for debugging and logging
        return f"User('{self.username}', '{self.email}')"

