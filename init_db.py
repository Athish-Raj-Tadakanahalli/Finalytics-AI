from app import create_app
from models import db

def setup_database():
    print("Creating tables for SQLite database...")
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")

if __name__ == "__main__":
    setup_database()
