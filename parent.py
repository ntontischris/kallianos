from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import User, Course, Enrollment, Grade, Message, db
from functools import wraps

parent_bp = Blueprint('parent', __name__)

def parent_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'parent':
            flash('Πρέπει να είστε γονέας για να δείτε αυτή τη σελίδα.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@parent_bp.route('/parent/dashboard')
@login_required
@parent_required
def dashboard():
    children = User.query.filter_by(parent_id=current_user.id).all()
    return render_template('parent/dashboard.html', children=children)

@parent_bp.route('/parent/link_student', methods=['GET', 'POST'])
@login_required
@parent_required
def link_student():
    if request.method == 'POST':
        student_email = request.form.get('student_email')
        if not student_email:
            flash('Παρακαλώ εισάγετε το email του μαθητή.', 'error')
            return redirect(url_for('parent.link_student'))
            
        student = User.query.filter_by(email=student_email, role='student').first()
        if not student:
            flash('Δεν βρέθηκε μαθητής με αυτό το email.', 'error')
            return redirect(url_for('parent.link_student'))
            
        if student.parent_id:
            flash('Ο μαθητής είναι ήδη συνδεδεμένος με άλλο γονέα.', 'error')
            return redirect(url_for('parent.link_student'))
            
        student.parent_id = current_user.id
        try:
            db.session.commit()
            flash('Ο μαθητής συνδέθηκε επιτυχώς με το λογαριασμό σας.', 'success')
            return redirect(url_for('parent.dashboard'))
        except:
            db.session.rollback()
            flash('Παρουσιάστηκε σφάλμα κατά τη σύνδεση.', 'error')
            
    return render_template('parent/link_student.html')

@parent_bp.route('/parent/student/<int:student_id>/progress')
@login_required
@parent_required
def student_progress(student_id):
    student = User.query.get_or_404(student_id)
    if student.parent_id != current_user.id:
        flash('Δεν έχετε πρόσβαση σε αυτόν τον μαθητή.', 'error')
        return redirect(url_for('parent.dashboard'))
        
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    return render_template('parent/student_progress.html', student=student, enrollments=enrollments)

@parent_bp.route('/parent/messages')
@login_required
@parent_required
def messages():
    messages_received = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    messages_sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('parent/messages.html', messages_received=messages_received, messages_sent=messages_sent)

@parent_bp.route('/parent/send_message', methods=['GET', 'POST'])
@login_required
@parent_required
def send_message():
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        body = request.form.get('body')
        
        if not all([recipient_id, subject, body]):
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία.', 'error')
            return redirect(url_for('parent.send_message'))
            
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            subject=subject,
            body=body
        )
        
        try:
            db.session.add(message)
            db.session.commit()
            flash('Το μήνυμα στάλθηκε επιτυχώς.', 'success')
            return redirect(url_for('parent.messages'))
        except:
            db.session.rollback()
            flash('Παρουσιάστηκε σφάλμα κατά την αποστολή του μηνύματος.', 'error')
            
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('parent/send_message.html', teachers=teachers)
