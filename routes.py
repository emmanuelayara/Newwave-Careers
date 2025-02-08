from flask import render_template, url_for, flash, redirect  # Flask utilities
from app import app, db, bcrypt  # Import app, database, and bcrypt
from models import User  # Import User model
from flask_bcrypt import check_password_hash  # Import bcrypt check function
from forms import RegistrationForm  # Import RegistrationForm
from flask_login import login_user  # For logging in users
from flask import render_template
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app import app, db
from models import User  # Import the User model
from forms import LoginForm  # ✅ Add this line


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Create an instance of the registration form

    if form.validate_on_submit():  # Check if the form is valid when submitted
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # Create new user
        db.session.add(user)  # Add user to database
        db.session.commit()  # Save changes

        flash('Your account has been created! You can now log in.', 'success')  # Success message
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('register.html', title='Register', form=form)  # Render the registration page


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Assuming you're using a login form

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Find user by email

        if user and bcrypt.check_password_hash(user.password, form.password.data):  # ✅ Check hashed password
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))
    
    return f"Welcome to your dashboard, {session['user_email']}!"

