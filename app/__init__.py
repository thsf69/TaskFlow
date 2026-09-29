import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-prod')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///taskflow.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'views.login'

    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from app.routes.api_auth import api_auth_bp
    from app.routes.api_tasks import api_tasks_bp
    from app.routes.views import views_bp

    app.register_blueprint(api_auth_bp, url_prefix='/api')
    app.register_blueprint(api_tasks_bp, url_prefix='/api')
    app.register_blueprint(views_bp)

    # Create db tables
    with app.app_context():
        db.create_all()

    return app
