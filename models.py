from app import db, login_manager  # Import from our app instance
from flask_login import UserMixin  # Provides default implementations for Flask-Login
from datetime import datetime  # For timestamping user creation
from enum import Enum
from app import db


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Query the User table by ID
    return User.query.get(int(user_id))


class UserRole(Enum):
    JOB_SEEKER = "JOB_SEEKER"
    EMPLOYER = "EMPLOYER"
    ADMIN = "ADMIN"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.JOB_SEEKER)
    profile_image = db.Column(db.String(200), nullable=True, default='default.jpg')

    # Job Relationships
    applications = db.relationship('Application', backref='applicant', lazy=True)
    saved_jobs = db.relationship('Job', secondary='saved_jobs', backref='saved_by', lazy='dynamic')

    def get_profile_image(self):
        return self.profile_image if self.profile_image else 'default.jpg'

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"


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
    applications = db.relationship('Application', backref='job_applications', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Job('{self.title}', '{self.company}')"


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cover_letter = db.Column(db.String(255), nullable=False)  # Store file path
    upload_resume = db.Column(db.String(255), nullable=False)  # Store file path
    other_documents = db.Column(db.String(255), nullable=True)  # Optional file path
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)

job = db.relationship('Job', backref=db.backref('job_applications', lazy=True), lazy=True)
user = db.relationship('User', backref=db.backref('user_applications', lazy=True), lazy=True)


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    profile_summary = db.Column(db.Text, nullable=True)  # Profile Summary
    activities_interests = db.Column(db.Text, nullable=True)  # List of activities
    key_skills = db.Column(db.Text, nullable=True)  # List of skills
    education = db.relationship("Education", backref="resume", lazy=True, cascade="all, delete-orphan")  # Multiple entries
    experience = db.relationship("WorkExperience", backref="resume", lazy=True, cascade="all, delete-orphan")  # Multiple entries

    user = db.relationship("User", backref="resume", uselist=False)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=False)
    degree = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(50), nullable=False)

class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=False)
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    start_year = db.Column(db.String(50), nullable=False)
    end_year = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Establish relationship (if not already defined in User model)
    user = db.relationship('User', backref='notifications', lazy=True)

    def __repr__(self):
        return f"Notification('{self.message}', Read: {self.read})"
