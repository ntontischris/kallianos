from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from models import User, Course, Enrollment, Grade, Activity, db
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Πρέπει να είστε διαχειριστής για να δείτε αυτή τη σελίδα.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    # Get user statistics
    total_users = User.query.count()
    students = User.query.filter_by(role='student').count()
    teachers = User.query.filter_by(role='teacher').count()
    parents = User.query.filter_by(role='parent').count()
    
    # Get course statistics
    total_courses = Course.query.count()
    active_enrollments = Enrollment.query.count()
    
    # Get activity statistics for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_activities = Activity.query.filter(Activity.timestamp >= thirty_days_ago).count()
    
    # Get daily user activity for the last 30 days
    daily_activity = db.session.query(
        func.date(Activity.timestamp).label('date'),
        func.count(Activity.id).label('count')
    ).filter(
        Activity.timestamp >= thirty_days_ago
    ).group_by(
        func.date(Activity.timestamp)
    ).all()
    
    # Prepare data for charts
    activity_dates = [str(record.date) for record in daily_activity]
    activity_counts = [record.count for record in daily_activity]
    
    # Get average grades per course
    course_grades = db.session.query(
        Course.title,
        func.avg(Grade.score / Grade.max_score * 100).label('avg_grade')
    ).join(
        Enrollment, Course.id == Enrollment.course_id
    ).join(
        Grade, Enrollment.id == Grade.enrollment_id
    ).group_by(
        Course.title
    ).all()
    
    course_names = [record.title for record in course_grades]
    avg_grades = [float(record.avg_grade or 0) for record in course_grades]
    
    # Get user distribution data
    user_distribution = {
        'Students': students,
        'Teachers': teachers,
        'Parents': parents
    }
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_courses=total_courses,
                         active_enrollments=active_enrollments,
                         recent_activities=recent_activities,
                         activity_dates=activity_dates,
                         activity_counts=activity_counts,
                         course_names=course_names,
                         avg_grades=avg_grades,
                         user_distribution=user_distribution)
