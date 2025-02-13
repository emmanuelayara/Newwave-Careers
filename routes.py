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
from flask_login import login_required, current_user
from flask_login import logout_user
from models import Job  # Ensure Job is imported
from models import Application  # Ensure Application is imported
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash



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

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)  # This properly logs in the user

            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/post-job", methods=['GET', 'POST'])
@login_required
def post_job():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        company = request.form.get('company')
        location = request.form.get('location')

        new_job = Job(title=title, description=description, company=company, location=location)
        db.session.add(new_job)
        db.session.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('post_job.html')


@app.route("/apply/<int:job_id>", methods=['GET', 'POST'])
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter')

        new_application = Application(job_id=job.id, user_id=current_user.id, cover_letter=cover_letter)
        db.session.add(new_application)
        db.session.commit()
        
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('jobs'))

    return render_template('apply.html', job=job)


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('dashboard'))

    users = User.query.all()
    jobs = Job.query.all()
    return render_template('admin.html', users=users, jobs=jobs)


@app.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('admin_dashboard'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_job/<int:job_id>')
@login_required
def delete_job(job_id):
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('admin_dashboard'))

    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))


@app.route("/jobs")
def jobs():
    job_list = Job.query.all()
    return render_template('jobs.html', jobs=job_list)



@app.route("/dashboard")
@login_required  # Ensures only logged-in users can access it
def dashboard():
    return render_template('dashboard.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
