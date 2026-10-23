import os
try:
    from dotenv import load_dotenv
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))
except ImportError:
    basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'finalytics-production-fallback-key-2024'
    
    # Handle PostgreSQL URL (Render/Heroku often supply 'postgres://', SQLAlchemy requires 'postgresql://')
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = database_url or ('sqlite:///' + os.path.join(basedir, 'finance.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

