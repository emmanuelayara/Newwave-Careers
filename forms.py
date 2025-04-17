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
from wtforms import StringField, TextAreaField, SubmitField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired



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
    
    role = SelectField('Role', choices=[( 'JOB_SEEKER'), ('EMPLOYER')],
                      validators=[DataRequired()])

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


class EducationForm(FlaskForm):
    degree = StringField("Degree", validators=[DataRequired()])
    institution = StringField("Institution", validators=[DataRequired()])
    year = StringField("Year of Graduation", validators=[DataRequired()])

class WorkExperienceForm(FlaskForm):
    job_title = StringField("Job Title", validators=[DataRequired()])
    company = StringField("Company", validators=[DataRequired()])
    location = StringField("Location")
    start_year = StringField("Start Year", validators=[DataRequired()])
    end_year = StringField("End Year (or 'Present')")
    description = TextAreaField("Description")

class ResumeForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    profile_summary = TextAreaField("Profile Summary")
    activities_interests = TextAreaField("Activities & Interests (Comma-separated)")
    key_skills = TextAreaField("Key Skills (Comma-separated)")
    
    education = FieldList(FormField(EducationForm), min_entries=1)
    experience = FieldList(FormField(WorkExperienceForm), min_entries=1)

    submit = SubmitField("Save Resume")


class ApplicationForm(FlaskForm):
    cover_letter = TextAreaField("Cover Letter", validators=[DataRequired()])
    upload_resume = FileField("Upload Resume (PDF/DOCX)", 
                       validators=[FileRequired(), FileAllowed(['pdf', 'docx'], 'PDF and DOCX only!')])
    other_documents = FileField("Upload Additional Documents (Optional - PDF/DOCX)", 
                                validators=[FileAllowed(['pdf', 'docx'], 'PDF and DOCX only!')])
    submit = SubmitField("Submit Application")


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio')
    location = StringField('Location')
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Update Profile')


class EmployerProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Who are We?')
    location = StringField('Location')
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Update Profile')



class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(min=3, max=100)])
    company = StringField('Company', validators=[DataRequired(), Length(min=2, max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Job Description', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit')


class QuestionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    option_a = StringField('Option A', validators=[DataRequired()])
    option_b = StringField('Option B', validators=[DataRequired()])
    option_c = StringField('Option C', validators=[DataRequired()])
    option_d = StringField('Option D', validators=[DataRequired()])
    correct_option = SelectField('Correct Option', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], validators=[DataRequired()])

class AddTestForm(FlaskForm):
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    submit = SubmitField('Submit Test')
