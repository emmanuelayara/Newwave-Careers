from flask import Flask  # Core Flask functionality
from flask_sqlalchemy import SQLAlchemy  # ORM for database interactions
from flask_bcrypt import Bcrypt  # For hashing passwords
from flask_login import LoginManager  # Manages user sessions
from flask_migrate import Migrate

app = Flask(__name__)


# Secret key for session management and CSRF protection
app.config['SECRET_KEY'] = 'newwavecareers'  # Replace with a strong secret key

# Database configuration (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newwave.db'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
bcrypt = Bcrypt(app)  # ✅ Initialize bcrypt
login_manager = LoginManager(app)

# Configure the login view and message category
login_manager.login_view = 'login'  # Redirect to login page if not authenticated
login_manager.login_message_category = 'info'  # Bootstrap class for flash messages

# Import routes (to be created later)
from routes import *

if __name__ == '__main__':
    # Run the Flask application in debug mode for development
    app.run(debug=True)