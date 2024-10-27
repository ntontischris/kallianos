from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import Course, User, Enrollment, Grade, Activity, db
from flask_login import login_required, current_user
from datetime import datetime, timedelta

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses')
def index():
    courses = Course.query.all()
    teachers = {
        course.teacher_id: User.query.get(course.teacher_id).username 
        for course in courses if course.teacher_id
    }
    return render_template('courses/index.html', courses=courses, teachers=teachers)

@courses_bp.route('/courses/<int:id>')
@login_required
def view(id):
    course = Course.query.get_or_404(id)
    teacher = User.query.get(course.teacher_id) if course.teacher_id else None
    is_enrolled = False
    if current_user.is_authenticated and current_user.role == 'student':
        is_enrolled = Enrollment.query.filter_by(
            student_id=current_user.id,
            course_id=course.id
        ).first() is not None
    return render_template('courses/view.html', 
                         course=course, 
                         teacher=teacher,
                         is_enrolled=is_enrolled)

@courses_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll(course_id):
    if current_user.role != 'student':
        flash('Μόνο οι μαθητές μπορούν να εγγραφούν σε μαθήματα.', 'error')
        return redirect(url_for('courses.view', id=course_id))
    
    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing_enrollment:
        flash('Είστε ήδη εγγεγραμμένος/η σε αυτό το μάθημα.', 'info')
        return redirect(url_for('courses.view', id=course_id))
    
    # Create new enrollment
    enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
    db.session.add(enrollment)
    
    # Record activity
    activity = Activity(
        user_id=current_user.id,
        activity_type='enrollment',
        description=f'Εγγραφή στο μάθημα: {Course.query.get(course_id).title}'
    )
    db.session.add(activity)
    
    try:
        db.session.commit()
        flash('Η εγγραφή σας ολοκληρώθηκε με επιτυχία!', 'success')
    except:
        db.session.rollback()
        flash('Παρουσιάστηκε σφάλμα κατά την εγγραφή.', 'error')
    
    return redirect(url_for('courses.view', id=course_id))

@courses_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return redirect(url_for('courses.index'))
    
    # Get student's enrollments
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    
    # Get recent activities
    activities = Activity.query.filter_by(user_id=current_user.id)\
        .order_by(Activity.timestamp.desc())\
        .limit(10).all()
    
    # Prepare chart data
    dates = []
    progress_data = []
    start_date = datetime.utcnow() - timedelta(days=30)
    
    # Sample progress data (replace with actual logic)
    for i in range(31):
        current_date = start_date + timedelta(days=i)
        dates.append(current_date.strftime('%d/%m'))
        progress_data.append(min(100, i * 3.33))  # Sample progress calculation
    
    return render_template('dashboard.html',
                         enrollments=enrollments,
                         activities=activities,
                         chart_labels=dates,
                         chart_data=progress_data)
