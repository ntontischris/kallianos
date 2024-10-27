from app import app, db
from models import User, Course
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create test parent
        test_parent = User(
            username='test_parent',
            email='parent@example.com',
            role='parent',
            password_hash=generate_password_hash('test123')
        )
        db.session.add(test_parent)
        db.session.commit()  # Commit to get the parent ID
        
        # Create test student linked to parent
        test_student = User(
            username='test_student',
            email='student@example.com',
            role='student',
            parent_id=test_parent.id,
            password_hash=generate_password_hash('test123')
        )
        db.session.add(test_student)
        
        # Create test teacher
        test_teacher = User(
            username='test_teacher',
            email='teacher@example.com',
            role='teacher',
            password_hash=generate_password_hash('test123')
        )
        db.session.add(test_teacher)
        
        # Create test course
        test_course = Course(
            title='Αρχαία Ελληνικά',
            description='Εισαγωγή στη γλώσσα και τον πολιτισμό της αρχαίας Ελλάδας',
            teacher_id=3  # This will be the teacher's ID
        )
        db.session.add(test_course)
        
        try:
            db.session.commit()
            print("Database initialized successfully with test data!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()
