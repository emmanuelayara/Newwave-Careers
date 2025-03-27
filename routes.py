from flask import render_template, url_for, flash, redirect  # Flask utilities
from app import app, db, bcrypt  # Import app, database, and bcrypt
from models import User  # Import User model
from models import Education
from models import WorkExperience
from models import Resume
import pdfkit
from flask import render_template, Response
from xhtml2pdf import pisa
import io
from flask import render_template, Response, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Resume  # Ensure your Resume model is imported
import io
from flask import Response, flash, redirect, url_for
from flask_login import login_required, current_user
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from forms import ResumeForm
from flask_bcrypt import check_password_hash  # Import bcrypt check function
from forms import RegistrationForm  # Import RegistrationForm
from flask_login import login_user  # For logging in users
from flask import render_template
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from models import Resume
from forms import ResumeForm
from models import User  # Import the User model
from forms import LoginForm  # ✅ Add this line
from flask_login import login_required, current_user
from flask_login import logout_user
from models import Job  # Ensure Job is imported
from models import Application  # Ensure Application is imported
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash
from flask import make_response
import io
from flask import Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import app, db
from forms import ProfileForm
import os
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import app, db
from forms import ProfileForm
from flask import render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from models import Notification
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']




@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route('/notifications')
@login_required
def notifications():
    # Retrieve all notifications for the current user, ordered by most recent
    notifications = Notification.query.filter_by(user_id=current_user.id)\
                                        .order_by(Notification.timestamp.desc())\
                                        .all()
    return render_template('notifications.html', notifications=notifications)


@app.route('/notifications/read/<int:notification_id>')
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    # Ensure that the notification belongs to the current user
    if notification.user_id != current_user.id:
        abort(403)
    notification.read = True
    db.session.commit()
    flash('Notification marked as read.', 'success')
    return redirect(url_for('notifications'))


@app.route('/notifications/delete/<int:notification_id>')
@login_required
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        abort(403)
    db.session.delete(notification)
    db.session.commit()
    flash('Notification deleted.', 'success')
    return redirect(url_for('notifications'))


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



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Update text fields
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        
        # Handle profile image upload if provided
        if form.profile_image.data:
            file = form.profile_image.data
            if file and allowed_file(file.filename):
                # Create a secure filename
                filename = secure_filename(file.filename)
                # Optionally, prepend user id or username to the filename to avoid collisions
                filename = f"user_{current_user.id}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                # Save the filename in the database (relative path)
                current_user.profile_image = filename

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to dashboard after updating profile
    elif request.method == 'GET':
        # Pre-populate form with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.location.data = current_user.location

    return render_template('profile.html', form=form)



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


@app.route("/resume", methods=["GET", "POST"])
def resume():
    form = ResumeForm()
    
    if request.method == "GET":
        if not form.education.data:
            form.education.append_entry()
        if not form.experience.data:
            form.experience.append_entry()

    if form.validate_on_submit():
        flash("Form validated successfully!", "info")
    else:
        print(form.errors)  # Add this line
        if request.method == "POST":
            resume = Resume(
                user_id=current_user.id,
                full_name=form.full_name.data,
                phone=form.phone.data,
                email=form.email.data,
                profile_summary=form.profile_summary.data,
                activities_interests=form.activities_interests.data,
                key_skills=form.key_skills.data
            )
            db.session.add(resume)
            db.session.commit()

            # Add Education Entries
            for edu in form.education.data:
                education = Education(
                    degree=edu["degree"],
                    institution=edu["institution"],
                    year=edu["year"],
                    resume_id=resume.id
                )
                db.session.add(education)

            # Add Work Experience Entries
            for exp in form.experience.data:
                experience = WorkExperience(
                    job_title=exp["job_title"],
                    company=exp["company"],
                    location=exp["location"],
                    start_year=exp["start_year"],
                    end_year=exp["end_year"],
                    description=exp["description"],
                    resume_id=resume.id
                )
                db.session.add(experience)

            db.session.commit()
            flash("Resume saved successfully!", "success")
           
            return redirect(url_for("resume_preview"))
    
    return render_template("resume.html", form=form)


@app.route("/resume/preview")
@login_required
def resume_preview():
    # Get the current user's resume
    resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.id.desc()).first()
    if not resume:
        flash("You have not created a resume yet.", "warning")
        return redirect(url_for("resume"))
    
    education = Education.query.filter_by(resume_id=resume.id).all()
    experience = WorkExperience.query.filter_by(resume_id=resume.id).all()

    return render_template("resume_preview.html", resume=resume, education=education, experience=experience)



@app.route("/resume/download")
@login_required
def resume_download():
    # Retrieve the current user's resume
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    if not resume:
        flash("You have not created a resume yet.", "warning")
        return redirect(url_for("resume"))

    # Render the HTML template as a string
    html = render_template("resume_preview.html", resume=resume)

    # Create a BytesIO buffer to hold the PDF
    buffer = io.BytesIO()

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=buffer)

    if pisa_status.err:
        flash("Error generating PDF", "danger")
        return redirect(url_for("resume"))

    # Move buffer position to the beginning
    buffer.seek(0)

    return Response(buffer, mimetype="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=resume.pdf"})





@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
