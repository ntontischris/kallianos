from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import User, Course, Enrollment, Grade, db
from functools import wraps

teacher_bp = Blueprint('teacher', __name__)

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            flash('Πρέπει να είστε καθηγητής για να δείτε αυτή τη σελίδα.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/teacher/dashboard')
@login_required
@teacher_required
def dashboard():
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/dashboard.html', courses=courses)

@teacher_bp.route('/teacher/course/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_course():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('Παρακαλώ συμπληρώστε τον τίτλο του μαθήματος.', 'error')
            return redirect(url_for('teacher.create_course'))
            
        course = Course(title=title, description=description, teacher_id=current_user.id)
        
        try:
            db.session.add(course)
            db.session.commit()
            flash('Το μάθημα δημιουργήθηκε με επιτυχία!', 'success')
            return redirect(url_for('teacher.dashboard'))
        except:
            db.session.rollback()
            flash('Παρουσιάστηκε σφάλμα κατά τη δημιουργία του μαθήματος.', 'error')
            
    return render_template('teacher/create_course.html')

@teacher_bp.route('/teacher/course/<int:course_id>')
@login_required
@teacher_required
def view_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        flash('Δεν έχετε πρόσβαση σε αυτό το μάθημα.', 'error')
        return redirect(url_for('teacher.dashboard'))
        
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    students = []
    for enrollment in enrollments:
        student = User.query.get(enrollment.student_id)
        grades = Grade.query.filter_by(enrollment_id=enrollment.id).all()
        students.append({
            'user': student,
            'enrollment': enrollment,
            'grades': grades
        })
        
    return render_template('teacher/view_course.html', course=course, students=students)

@teacher_bp.route('/teacher/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        flash('Δεν έχετε πρόσβαση σε αυτό το μάθημα.', 'error')
        return redirect(url_for('teacher.dashboard'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('Παρακαλώ συμπληρώστε τον τίτλο του μαθήματος.', 'error')
            return redirect(url_for('teacher.edit_course', course_id=course_id))
            
        try:
            course.title = title
            course.description = description
            db.session.commit()
            flash('Το μάθημα ενημερώθηκε με επιτυχία!', 'success')
            return redirect(url_for('teacher.view_course', course_id=course_id))
        except:
            db.session.rollback()
            flash('Παρουσιάστηκε σφάλμα κατά την ενημέρωση του μαθήματος.', 'error')
            
    return render_template('teacher/edit_course.html', course=course)
