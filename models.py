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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    profile_image = db.Column(db.String(200), nullable=True, default='default.jpg')
    
    # Optionally, relationships for application history and saved jobs:
    applications = db.relationship('Application', backref='applicant', lazy=True)
    saved_jobs = db.relationship('Job', secondary='saved_jobs', backref='saved_by', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

saved_jobs = db.Table('saved_jobs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'))
)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship('Application', backref='job', lazy=True)


    def __repr__(self):
        return f"Job('{self.title}', '{self.company}')"


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    education = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    Awards_and_honors = db.Column(db.Text, nullable=True)
    
    user = db.relationship("User", backref="resume", uselist=False)
