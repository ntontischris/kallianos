from app import app, db
from models import User, Course
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(
                username='test_user',
                email='test@example.com',
                role='student',
                password_hash=generate_password_hash('test123')
            )
            db.session.add(test_user)
            
        # Create test course
        test_course = Course.query.filter_by(title='Αρχαία Ελληνικά').first()
        if not test_course:
            test_course = Course(
                title='Αρχαία Ελληνικά',
                description='Εισαγωγή στη γλώσσα και τον πολιτισμό της αρχαίας Ελλάδας',
                teacher_id=1
            )
            db.session.add(test_course)
            
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
