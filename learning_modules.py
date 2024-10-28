from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import LearningModule, ModuleProgress, ModuleQuestion, Course, Activity, db
from datetime import datetime

modules_bp = Blueprint('modules', __name__)

@modules_bp.route('/course/<int:course_id>/modules')
@login_required
def list_modules(course_id):
    course = Course.query.get_or_404(course_id)
    modules = LearningModule.query.filter_by(course_id=course_id).order_by(LearningModule.order).all()
    
    # Get progress for current student
    progress_data = {}
    if current_user.role == 'student':
        progress = ModuleProgress.query.filter_by(
            student_id=current_user.id
        ).all()
        progress_data = {p.module_id: p for p in progress}
    
    return render_template('modules/list.html', 
                         course=course, 
                         modules=modules,
                         progress_data=progress_data)

@modules_bp.route('/module/<int:module_id>')
@login_required
def view_module(module_id):
    module = LearningModule.query.get_or_404(module_id)
    
    # Get or create progress record for student
    progress = None
    if current_user.role == 'student':
        progress = ModuleProgress.query.filter_by(
            student_id=current_user.id,
            module_id=module_id
        ).first()
        
        if not progress:
            progress = ModuleProgress(
                student_id=current_user.id,
                module_id=module_id
            )
            db.session.add(progress)
            db.session.commit()
    
    return render_template('modules/view.html', 
                         module=module,
                         progress=progress)

@modules_bp.route('/module/<int:module_id>/complete', methods=['POST'])
@login_required
def complete_module(module_id):
    if current_user.role != 'student':
        return jsonify({'error': 'Only students can complete modules'}), 403
    
    progress = ModuleProgress.query.filter_by(
        student_id=current_user.id,
        module_id=module_id
    ).first()
    
    if not progress:
        progress = ModuleProgress(
            student_id=current_user.id,
            module_id=module_id
        )
        db.session.add(progress)
    
    progress.completed = True
    progress.last_interaction = datetime.utcnow()
    progress.attempts += 1
    
    # Record activity
    activity = Activity(
        user_id=current_user.id,
        activity_type='module_completion',
        description=f'Completed module: {progress.module.title}'
    )
    db.session.add(activity)
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'error': 'Error updating progress'}), 500

@modules_bp.route('/module/<int:module_id>/submit-quiz', methods=['POST'])
@login_required
def submit_quiz(module_id):
    if current_user.role != 'student':
        return jsonify({'error': 'Only students can submit quizzes'}), 403
    
    module = LearningModule.query.get_or_404(module_id)
    if module.module_type != 'quiz':
        return jsonify({'error': 'This module is not a quiz'}), 400
    
    answers = request.json.get('answers', {})
    questions = {str(q.id): q for q in module.questions}
    
    total_points = sum(q.points for q in module.questions)
    earned_points = 0
    
    for q_id, answer in answers.items():
        if q_id in questions:
            question = questions[q_id]
            if question.question_type == 'multiple_choice':
                if answer == question.correct_answer:
                    earned_points += question.points
            else:  # text answer - implement more sophisticated comparison if needed
                if answer.lower().strip() == question.correct_answer.lower().strip():
                    earned_points += question.points
    
    score = (earned_points / total_points) * 100 if total_points > 0 else 0
    
    progress = ModuleProgress.query.filter_by(
        student_id=current_user.id,
        module_id=module_id
    ).first()
    
    if not progress:
        progress = ModuleProgress(
            student_id=current_user.id,
            module_id=module_id
        )
        db.session.add(progress)
    
    progress.score = score
    progress.completed = True
    progress.last_interaction = datetime.utcnow()
    progress.attempts += 1
    
    activity = Activity(
        user_id=current_user.id,
        activity_type='quiz_completion',
        description=f'Completed quiz: {module.title} with score {score:.1f}%'
    )
    db.session.add(activity)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'score': score,
            'total_points': total_points,
            'earned_points': earned_points
        })
    except:
        db.session.rollback()
        return jsonify({'error': 'Error updating progress'}), 500
