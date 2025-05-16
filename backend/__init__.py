from flask import Flask, redirect, url_for
from flask_login import LoginManager
from .models import db
from .config import Config
from flask import session
from backend.models import User
import os
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder='../frontend',
        static_folder='../frontend',
    )

    # Use TestConfig when in testing mode
    if os.environ.get('FLASK_ENV') == 'testing':
        from .config import TestConfig
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(config_class)
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Define user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Inject `user` into all templates
    @app.context_processor
    def inject_user():
        user = None
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            # Check if user exists before accessing avatar path
            if user and not user.avatar_path:
                user.avatar_path = 'asset/avatar.png'
        return dict(user=user)

    # Import routes before registering blueprint
    from . import routes
    
    # Register blueprint
    from .blueprints import main
    app.register_blueprint(main, url_prefix='/main')
    
    # Add root route redirect
    @app.route('/')
    def index():
        return redirect(url_for('main.home'))

    return app
