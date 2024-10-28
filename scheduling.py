from datetime import datetime
from flask import Blueprint, jsonify, request
from models import db, Schedule, Appointment

scheduling_bp = Blueprint('scheduling', __name__)

@scheduling_bp.route('/schedule', methods=['GET'])
def get_schedule():
    """Retrieve the schedule for a specific user or course."""
    user_id = request.args.get('user_id')
    course_id = request.args.get('course_id')
    if not user_id and not course_id:
        return jsonify({'error': 'User ID or Course ID must be provided'}), 400

    schedule = Schedule.query.filter_by(user_id=user_id, course_id=course_id).all()
    return jsonify([s.to_dict() for s in schedule])

@scheduling_bp.route('/schedule', methods=['POST'])
def create_schedule():
    """Create a new schedule entry."""
    data = request.json
    user_id = data.get('user_id')
    course_id = data.get('course_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([user_id, course_id, start_time, end_time]):
        return jsonify({'error': 'All fields are required'}), 400

    new_schedule = Schedule(user_id=user_id, course_id=course_id, start_time=start_time, end_time=end_time)
    db.session.add(new_schedule)
    db.session.commit()
    return jsonify(new_schedule.to_dict()), 201

@scheduling_bp.route('/appointment', methods=['POST'])
def create_appointment():
    """Create a new appointment."""
    data = request.json
    user_id = data.get('user_id')
    date = data.get('date')
    time = data.get('time')
    description = data.get('description')

    if not all([user_id, date, time, description]):
        return jsonify({'error': 'All fields are required'}), 400

    new_appointment = Appointment(user_id=user_id, date=date, time=time, description=description)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(new_appointment.to_dict()), 201

@scheduling_bp.route('/appointment', methods=['GET'])
def get_appointments():
    """Retrieve appointments for a specific user."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID must be provided'}), 400

    appointments = Appointment.query.filter_by(user_id=user_id).all()
    return jsonify([a.to_dict() for a in appointments])
