from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from werkzeug.security import check_password_hash, generate_password_hash
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        return redirect(url_for('courses.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία.', 'error')
            return render_template('auth/login.html')
            
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.role == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            return redirect(url_for('courses.index'))
            
        flash('Λάθος email ή κωδικός πρόσβασης.', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία.', 'error')
            return render_template('auth/register_teacher.html')
            
        if password != confirm_password:
            flash('Οι κωδικοί δεν ταιριάζουν.', 'error')
            return render_template('auth/register_teacher.html')
            
        if User.query.filter_by(email=email).first():
            flash('Το email χρησιμοποιείται ήδη.', 'error')
            return render_template('auth/register_teacher.html')
            
        if User.query.filter_by(username=username).first():
            flash('Το όνομα χρήστη χρησιμοποιείται ήδη.', 'error')
            return render_template('auth/register_teacher.html')
            
        user = User(username=username, email=email, role='teacher')
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Η εγγραφή ολοκληρώθηκε με επιτυχία! Μπορείτε να συνδεθείτε.', 'success')
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('Παρουσιάστηκε σφάλμα κατά την εγγραφή.', 'error')
            
    return render_template('auth/register_teacher.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Αποσυνδεθήκατε επιτυχώς.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    if (new_password or email != current_user.email) and not current_user.check_password(current_password):
        flash('Ο τρέχων κωδικός είναι λάθος.', 'error')
        return redirect(url_for('auth.profile'))

    if email != current_user.email and User.query.filter_by(email=email).first():
        flash('Το email χρησιμοποιείται ήδη.', 'error')
        return redirect(url_for('auth.profile'))

    current_user.username = username
    current_user.email = email
    if new_password:
        current_user.set_password(new_password)

    try:
        db.session.commit()
        flash('Το προφίλ ενημερώθηκε επιτυχώς.', 'success')
    except:
        db.session.rollback()
        flash('Παρουσιάστηκε σφάλμα κατά την ενημέρωση.', 'error')

    return redirect(url_for('auth.profile'))

@auth_bp.route('/profile/upload-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        flash('Δεν επιλέχθηκε αρχείο.', 'error')
        return redirect(url_for('auth.profile'))

    file = request.files['profile_picture']
    if file.filename == '':
        flash('Δεν επιλέχθηκε αρχείο.', 'error')
        return redirect(url_for('auth.profile'))

    if file:
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/uploads/profile_pictures', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            
            current_user.profile_picture = '/' + file_path
            db.session.commit()
            flash('Η φωτογραφία προφίλ ενημερώθηκε επιτυχώς.', 'success')
        except:
            db.session.rollback()
            flash('Παρουσιάστηκε σφάλμα κατά το ανέβασμα της φωτογραφίας.', 'error')

    return redirect(url_for('auth.profile'))
