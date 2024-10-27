from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from config import Config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from auth import auth_bp
    from courses import courses_bp
    from teacher import teacher_bp
    from parent import parent_bp
    from messages import messages_bp
    from routes.ai import ai_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(parent_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(ai_bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    with app.app_context():
        import models
        db.create_all()
        
    return app

app = create_app()

@login_manager.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))
