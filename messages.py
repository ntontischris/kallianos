from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import Message, User, db
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages')
@login_required
def index():
    messages_received = Message.query.filter_by(recipient_id=current_user.id)\
        .order_by(Message.timestamp.desc()).all()
    messages_sent = Message.query.filter_by(sender_id=current_user.id)\
        .order_by(Message.timestamp.desc()).all()
    
    # Get list of teachers for parents, or parents for teachers
    if current_user.role == 'parent':
        recipients = User.query.filter_by(role='teacher').all()
    elif current_user.role == 'teacher':
        recipients = User.query.filter_by(role='parent').all()
    else:
        recipients = []
    
    return render_template('messages/index.html',
                         messages_received=messages_received,
                         messages_sent=messages_sent,
                         recipients=recipients)

@messages_bp.route('/messages/send', methods=['POST'])
@login_required
def send_message():
    recipient_id = request.form.get('recipient_id')
    subject = request.form.get('subject')
    body = request.form.get('body')
    category = request.form.get('category', 'general')
    
    if not all([recipient_id, subject, body]):
        flash('Παρακαλώ συμπληρώστε όλα τα πεδία.', 'error')
        return redirect(url_for('messages.index'))
        
    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        subject=subject,
        body=body,
        category=category
    )
    
    try:
        db.session.add(message)
        db.session.commit()
        flash('Το μήνυμα στάλθηκε επιτυχώς.', 'success')
    except:
        db.session.rollback()
        flash('Παρουσιάστηκε σφάλμα κατά την αποστολή του μηνύματος.', 'error')
    
    return redirect(url_for('messages.index'))

@messages_bp.route('/messages/<int:message_id>/read', methods=['POST'])
@login_required
def mark_as_read(message_id):
    message = Message.query.get_or_404(message_id)
    if message.recipient_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    message.read = True
    db.session.commit()
    return jsonify({'success': True})

@messages_bp.route('/messages/unread-count')
@login_required
def unread_count():
    count = Message.query.filter_by(recipient_id=current_user.id, read=False).count()
    return jsonify({'count': count})
