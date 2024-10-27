from app import app, db
from models import User, Course  # Import all models to ensure they're registered

def reset_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Dropped all tables")
        
        # Recreate all tables
        db.create_all()
        print("Created all tables")

if __name__ == "__main__":
    reset_database()
