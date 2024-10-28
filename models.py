from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student, parent
    profile_picture = db.Column(db.String(255))  # Path to profile picture
    
    # Parent-Student relationship
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    children = db.relationship('User', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy=True)
    module_progress = db.relationship('ModuleProgress', backref='student', lazy=True)
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    modules = db.relationship('LearningModule', backref='course', lazy=True)

class LearningModule(db.Model):
    __tablename__ = 'learning_modules'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)  # For module sequence
    module_type = db.Column(db.String(50), nullable=False)  # 'text', 'quiz', 'interactive'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('ModuleProgress', backref='module', lazy=True)
    questions = db.relationship('ModuleQuestion', backref='module', lazy=True)

class ModuleQuestion(db.Model):
    __tablename__ = 'module_questions'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('learning_modules.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON)  # Store multiple choice options
    question_type = db.Column(db.String(50), nullable=False)  # 'multiple_choice', 'text'
    points = db.Column(db.Integer, default=1)

class ModuleProgress(db.Model):
    __tablename__ = 'module_progress'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('learning_modules.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float)  # For quiz/assessment modules
    last_interaction = db.Column(db.DateTime, default=datetime.utcnow)
    attempts = db.Column(db.Integer, default=0)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    grades = db.relationship('Grade', backref='enrollment', lazy=True)

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # enrollment, grade, etc.
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100))
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), default='general')  # homework, behavior, general
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
