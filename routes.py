from flask import render_template, url_for, flash, redirect, session  # Flask utilities
from app import app, db, bcrypt  # Import app, database, and bcrypt
from models import User  # Import User model
from flask_bcrypt import check_password_hash  # Import bcrypt check function
from forms import RegistrationForm  # Import RegistrationForm
from flask_login import login_user  # For logging in users
from flask import render_template
from flask import render_template, redirect
from werkzeug.security import check_password_hash
from app import app, db
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import User  # Import your User model
from app import app, db, bcrypt  # Import necessary modules
from werkzeug.security import check_password_hash
from models import User  # Import the User model
from forms import LoginForm  # Add this line


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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Make sure this exists in your forms.py

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)  # Pass form to the template




@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))
    
    return f"Welcome to your dashboard, {session['user_email']}!"

