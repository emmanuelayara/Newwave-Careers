from flask_wtf import FlaskForm  # Flask-WTF for form handling
from wtforms import StringField, PasswordField, SubmitField  # Form fields
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # Validators
from models import User  # Import User model

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=3, max=20)])  # Username field

    email = StringField('Email', 
                        validators=[DataRequired(), Email()])  # Email field

    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])  # Password field

    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])  # Confirm password

    submit = SubmitField('Sign Up')  # Submit button

    # Custom validation to check if username already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    # Custom validation to check if email already exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account with this email already exists.')
