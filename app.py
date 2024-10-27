from flask import Flask
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
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    
    with app.app_context():
        import models
        db.create_all()
        
    return app

app = create_app()

@login_manager.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))
