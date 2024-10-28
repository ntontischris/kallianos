from flask import Blueprint, jsonify, request
from models import db, Announcement, Notification, DirectMessage

communication_bp = Blueprint('communication', __name__)

@communication_bp.route('/announcements', methods=['GET'])
def get_announcements():
    """Retrieve all announcements."""
    announcements = Announcement.query.all()
    return jsonify([a.to_dict() for a in announcements])

@communication_bp.route('/announcements', methods=['POST'])
def create_announcement():
    """Create a new announcement."""
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not all([title, content]):
        return jsonify({'error': 'All fields are required'}), 400

    new_announcement = Announcement(title=title, content=content)
    db.session.add(new_announcement)
    db.session.commit()
    return jsonify(new_announcement.to_dict()), 201

@communication_bp.route('/notifications', methods=['GET'])
def get_notifications():
    """Retrieve notifications for a specific user."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID must be provided'}), 400

    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([n.to_dict() for n in notifications])

@communication_bp.route('/notifications', methods=['POST'])
def create_notification():
    """Create a new notification."""
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not all([user_id, message]):
        return jsonify({'error': 'All fields are required'}), 400

    new_notification = Notification(user_id=user_id, message=message)
    db.session.add(new_notification)
    db.session.commit()
    return jsonify(new_notification.to_dict()), 201

@communication_bp.route('/direct-messages', methods=['GET'])
def get_direct_messages():
    """Retrieve direct messages between two users."""
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    if not all([sender_id, receiver_id]):
        return jsonify({'error': 'Sender ID and Receiver ID must be provided'}), 400

    messages = DirectMessage.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).all()
    return jsonify([m.to_dict() for m in messages])

@communication_bp.route('/direct-messages', methods=['POST'])
def send_direct_message():
    """Send a direct message."""
    data = request.json
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    if not all([sender_id, receiver_id, content]):
        return jsonify({'error': 'All fields are required'}), 400

    new_message = DirectMessage(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201
