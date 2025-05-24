from flask import render_template, url_for, flash, redirect, abort, jsonify  # Flask utilities
from app import app, db, bcrypt  # Import app, database, and bcrypt
from models import User  # Import User model
from models import Education
from models import WorkExperience
from models import Resume
from functools import wraps
from slugify import slugify
from flask import abort
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app, db
from models import User
from models import BlogPost
from models import UserRole
from forms import RegistrationForm
from forms import EmployerProfileForm
from forms import QuestionForm
from forms import AddTestForm
from models import PreInterviewTest
from flask import render_template, Response
from xhtml2pdf import pisa
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from forms import ApplicationForm
from models import Application
import os
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
import os
from flask import request, flash, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'  # Set your uploads folder path
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']




@app.route("/")
def home():
    return render_template("home.html", title="Home", UserRole=UserRole)


app.route('/notifications')
@login_required
def employer_notifications():
    # Fetch notifications for current employer user, newest first
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return render_template('employer_notifications.html', notifications=notifications)

app.route('/notifications/read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        flash("You can't mark this notification.", "danger")
        return redirect(url_for('employer_notifications'))

    notification.is_read = True
    db.session.commit()
    flash('Notification marked as read.', 'success')
    return redirect(url_for('employer_notifications'))

app.route('/notifications/delete/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        flash("You can't delete this notification.", "danger")
        return redirect(url_for('employer_notifications'))

    db.session.delete(notification)
    db.session.commit()
    flash('Notification deleted.', 'success')
    return redirect(url_for('employer_notifications'))


@app.route('/notifications')
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=user_notifications, UserRole=UserRole)


@app.route('/notifications/read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        abort(403)
    notification.read = True
    db.session.commit()
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/notifications/read-all', methods=['POST'])
@login_required
def mark_all_notifications_as_read():
    notifications = Notification.query.filter_by(user_id=current_user.id, read=False).all()
    for note in notifications:
        note.read = True
    db.session.commit()
    return redirect(request.referrer or url_for('dashboard'))



@app.route('/notifications/delete/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        abort(403)
    db.session.delete(notification)
    db.session.commit()
    return redirect(request.referrer or url_for('dashboard'))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        role = form.role.data  # Get role from the form ('job_seeker' or 'employer')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form, UserRole=UserRole)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == UserRole.EMPLOYER:
                return redirect(url_for('employer_dashboard'))
            else:
                return redirect(url_for('dashboard'))

        flash('Invalid credentials', 'danger')

    return render_template('login.html', form=form, UserRole=UserRole)


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

    return render_template('profile.html', form=form, UserRole=UserRole)



@app.route('/employer_profile', methods=['GET', 'POST'])
@login_required
def employer_profile():
    form = EmployerProfileForm()
    
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
        return redirect(url_for('employer_dashboard'))  # Redirect to dashboard after updating profile
    elif request.method == 'GET':
        # Pre-populate form with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.location.data = current_user.location

    return render_template('employer_profile.html', form=form, UserRole=UserRole)


@app.route("/post-job", methods=['GET', 'POST'])
@login_required
def post_job():
    # Ensure only employers can access
    if current_user.role != UserRole.EMPLOYER:
        flash('Access denied: Only employers can post jobs.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        company = request.form.get('company')
        location = request.form.get('location')

        new_job = Job(
            title=title,
            description=description,
            company=company,
            location=location,
            user_id=current_user.id,
            employer_id=current_user.id
        )

        db.session.add(new_job)
        db.session.commit()

        # 🔔 Notify all job seekers about the new job
        job_seekers = User.query.filter_by(role=UserRole.JOB_SEEKER).all()
        for seeker in job_seekers:
            notification = Notification(
                user_id=seeker.id,
                message=f"New job posted: {new_job.title}",
            )
            db.session.add(notification)
        db.session.commit()

        flash('Job posted successfully!', 'success')
        return redirect(url_for('employer_dashboard'))

    return render_template('post_job.html', UserRole=UserRole)


@app.route("/apply/<int:job_id>", methods=['GET', 'POST'])
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    form = ApplicationForm()

    if form.validate_on_submit():
        cover_letter_text = form.cover_letter.data
        resume_file = form.upload_resume.data
        other_docs_file = form.other_documents.data

        # Ensure upload folder exists
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        def save_file(file):
            """Helper function to save file and return filename"""
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            return filename

        resume_path = save_file(resume_file)
        other_docs_path = save_file(other_docs_file) if other_docs_file else None

        # Save application to the database
        application = Application(
            job_id=job.id,
            user_id=current_user.id,
            cover_letter=cover_letter_text,
            upload_resume=resume_path,
            other_documents=other_docs_path
        )
        db.session.add(application)
        db.session.commit()

        # 🔔 Notify employer
        notification = Notification(
            user_id=job.employer_id,
            message=f"{current_user.username} applied to your job: {job.title}",
        )
        db.session.add(notification)
        db.session.commit()

        flash("Application submitted successfully!", "success")
        return redirect(url_for('jobs'))

    return render_template('apply.html', job=job, form=form, UserRole=UserRole)


@app.route('/employer/applicants/<int:job_id>')
@login_required
def view_applicants(job_id):
    job = Job.query.get_or_404(job_id)

    # Only allow the employer who posted the job to view applicants
    if current_user.id != job.employer_id:
        flash('You are not authorized to view applicants for this job.', 'danger')
        return redirect(url_for('employer_dashboard'))

    applicants = Application.query.filter_by(job_id=job_id).all()

    return render_template('view_applicants.html', job=job, applicants=applicants, UserRole=UserRole)



@app.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)

    # Only allow employers to edit their own job posts
    if job.employer_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        job.title = request.form.get('title')
        job.description = request.form.get('description')
        job.company = request.form.get('company')
        job.location = request.form.get('location')

        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('employer_dashboard'))

    return render_template('edit_job.html', job=job, UserRole=UserRole)


@app.route('/delete-job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    # Only allow employers to delete their own job posts
    if job.employer_id != current_user.id:
        abort(403)

    # Delete all related applications
    Application.query.filter_by(job_id=job.id).delete()

    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('employer_dashboard'))


@app.route("/jobs")
@login_required
def jobs():
    job_list = Job.query.all()
    return render_template('jobs.html', jobs=job_list, UserRole=UserRole)


@app.route("/dashboard")
@login_required
def dashboard():

    applications = current_user.applications.order_by(Application.date_applied.desc()).all()

    return render_template("dashboard.html", UserRole=UserRole, applications=applications)


@app.route("/employer_dashboard")
@login_required
def employer_dashboard():
    # Ensure only employers can access
    if current_user.role != UserRole.EMPLOYER:
        flash('Access denied: Employers only', 'danger')
        return redirect(url_for('home'))

    # Calculate total applications and total views for the employer's jobs
    total_applications = sum(len(job.applications) for job in current_user.jobs)

    # Check if views are being tracked in the Job model
    total_views = sum((job.views or 0) for job in current_user.jobs) if current_user.jobs and hasattr(current_user.jobs[0], 'views') else 0

    return render_template(
        "employer_dashboard.html",
        UserRole=UserRole,
        total_applications=total_applications,
        total_views=total_views
    )


@app.route('/manage_jobs')
@login_required
def manage_jobs():
    if current_user.role != UserRole.EMPLOYER:
        abort(403)

    jobs = Job.query.filter_by(employer_id=current_user.id).all()
    
    job_applications = {}
    for job in jobs:
        job_applications[job.id] = job.applications  # assuming job.applications is a relationship

    return render_template('manage_jobs.html', jobs=jobs, job_applications=job_applications, UserRole=UserRole)


@app.route('/add_test/<int:job_id>', methods=['GET', 'POST'])
@login_required
def add_test(job_id):
    job = Job.query.get_or_404(job_id)

    if job.employer_id != current_user.id:
        abort(403)

    form = AddTestForm()

    if form.validate_on_submit():
        for question_form in form.questions:
            question = PreInterviewTest(
                job_id=job_id,
                question=question_form.question.data,
                option_a=question_form.option_a.data,
                option_b=question_form.option_b.data,
                option_c=question_form.option_c.data,
                option_d=question_form.option_d.data,
                correct_option=question_form.correct_option.data
            )
            db.session.add(question)

        db.session.commit()
        flash('Pre-interview test added successfully!', 'success')
        return redirect(url_for('manage_jobs'))

    return render_template('add_test.html', form=form, job=job, UserRole=UserRole)



@app.route("/resume", methods=["GET", "POST"])
@login_required
def resume():
    form = ResumeForm()

    # Fetch existing resume if it exists
    resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.id.desc()).first()

    if request.method == "GET":
        if resume:
            # Populate personal details
            form.full_name.data = resume.full_name
            form.phone.data = resume.phone
            form.email.data = resume.email
            form.profile_summary.data = resume.profile_summary
            form.key_skills.data = resume.key_skills
            form.activities_interests.data = resume.activities_interests

            # Populate education
            form.education.entries = []  # Clear default entries
            for edu in resume.education:
                form.education.append_entry({
                    'degree': edu.degree,
                    'institution': edu.institution,
                    'year': edu.year
                })

            # Populate experience
            form.experience.entries = []  # Clear default entries
            for exp in resume.experience:
                form.experience.append_entry({
                    'job_title': exp.job_title,
                    'company': exp.company,
                    'location': exp.location,
                    'start_year': exp.start_year,
                    'end_year': exp.end_year,
                    'description': exp.description
                })
        else:
            # Add one blank entry if no existing data
            if not form.education.data:
                form.education.append_entry()
            if not form.experience.data:
                form.experience.append_entry()

    if form.validate_on_submit():
        # If editing existing resume, delete previous one
        if resume:
            Education.query.filter_by(resume_id=resume.id).delete()
            WorkExperience.query.filter_by(resume_id=resume.id).delete()
            db.session.delete(resume)
            db.session.commit()

        # Create new resume
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

        # Add new education
        for edu in form.education.data:
            education = Education(
                degree=edu["degree"],
                institution=edu["institution"],
                year=edu["year"],
                resume_id=resume.id
            )
            db.session.add(education)

        # Add new work experience
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
    else:
        print(form.errors)

    return render_template("resume.html", form=form, UserRole=UserRole)



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

    return render_template("resume_preview.html", resume=resume, education=education, experience=experience, UserRole=UserRole)



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



@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts, UserRole=UserRole)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug).first()
    if not post:
        abort(404)
    return render_template('blog_post.html', post=post, UserRole=UserRole)



@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        slug = slugify(title)  # you should have a slugify function

        new_post = BlogPost(title=title, content=content, slug=slug)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('create_post.html', UserRole=UserRole)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
