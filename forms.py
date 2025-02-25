from flask_wtf import FlaskForm  # Flask-WTF for form handling
from wtforms import StringField, PasswordField, SubmitField  # Form fields
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # Validators
from models import User  # Import User model
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


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


class ResumeForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    education = TextAreaField("Education", validators=[DataRequired()])
    experience = TextAreaField("Work Experience", validators=[DataRequired()])
    skills = TextAreaField("Skills", validators=[DataRequired()])
    summary = TextAreaField("Professional Summary")
    Awards_and_honors = TextAreaField("Awards and Honors")
    submit = SubmitField("Save Resume")



class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio')
    location = StringField('Location')
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Update Profile')



class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(min=3, max=100)])
    company = StringField('Company', validators=[DataRequired(), Length(min=2, max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Job Description', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit')
