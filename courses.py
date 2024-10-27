from flask import Blueprint, render_template
from models import Course, User
from flask_login import login_required

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
    return render_template('courses/view.html', course=course, teacher=teacher)
