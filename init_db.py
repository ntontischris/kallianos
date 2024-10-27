from app import app, db
from models import User, Course  # Import all models to ensure they're registered
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@edugreek.com',
            role='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin_user)
        
        # Create test parent
        test_parent = User(
            username='test_parent',
            email='parent@example.com',
            role='parent',
            password_hash=generate_password_hash('test123')
        )
        db.session.add(test_parent)
        
        # Create test student linked to parent
        test_student = User(
            username='test_student',
            email='student@example.com',
            role='student',
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
        
        # Commit to get the IDs
        db.session.commit()
        
        # Now update the student with parent_id
        test_student.parent_id = test_parent.id
        
        # Create test course
        test_course = Course(
            title='Αρχαία Ελληνικά',
            description='Εισαγωγή στη γλώσσα και τον πολιτισμό της αρχαίας Ελλάδας',
            teacher_id=test_teacher.id
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
