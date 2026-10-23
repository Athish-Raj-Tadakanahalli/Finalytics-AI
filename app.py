from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    from routes.transactions import transactions_bp
    app.register_blueprint(transactions_bp)
    
    from routes.budgets import budgets_bp
    app.register_blueprint(budgets_bp)
    
    # Automatically initialize tables in production/development
    with app.app_context():
        db.create_all()
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


