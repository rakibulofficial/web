    import os
from werkzeug.utils import secure_filename

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import Config
from models import db, Admin, Member, GalleryImage, Feedback
from forms import LoginForm, FeedbackForm

app = Flask(_name_)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        fb = Feedback(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(fb)
        db.session.commit()
        flash('Feedback submitted successfully!')
        return redirect(url_for('feedback'))
    return render_template('feedback.html', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('admin/login.html', form=form)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



# ... আগের কোড একই থাকবে

@app.route('/admin/gallery', methods=['GET', 'POST'])
@login_required
def admin_gallery():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image = GalleryImage(filename=filename)
            db.session.add(image)
            db.session.commit()
            flash('Image uploaded!')
    images = GalleryImage.query.all()
    return render_template('admin/gallery.html', images=images)

@app.route('/admin/gallery/delete/<int:image_id>')
@login_required
def delete_gallery_image(image_id):
    image = GalleryImage.query.get(image_id)
    if image:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        db.session.delete(image)
        db.session.commit()
        flash('Image deleted!')
    return redirect(url_for('admin_gallery'))

@app.route('/admin/members', methods=['GET', 'POST'])
@login_required
def admin_members():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        member = Member(name=name, role=role)
        db.session.add(member)
        db.session.commit()
        flash('Member added!')
    members = Member.query.all()
    return render_template('admin/members.html', members=members)

@app.route('/admin/members/delete/<int:member_id>')
@login_required
def delete_member(member_id):
    member = Member.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
        flash('Member deleted!')
    return redirect(url_for('admin_members'))