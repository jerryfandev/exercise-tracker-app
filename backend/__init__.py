from flask import Flask
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
    csrf = CSRFProtect(app)  # "This 'entry point' enforces CSRF protection by generating and validating CSRF tokens for all requests."

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

    # ✅ Auto-create DB if it doesn't exist
    with app.app_context():
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            if not os.path.exists(db_path):
                print("🆕 Creating new database:", db_path)
                db.create_all()
            else:
                print("✅ Database already exists:", db_path)

    # 📌 Inject `user` into all templates
    @app.context_processor
    def inject_user():
        user = None
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            # Check if the user exists before accessing the avatar path.
            if user and not user.avatar_path:
                user.avatar_path = 'asset/avatar.png'
        return dict(user=user)

    from .routes import register_routes
    register_routes(app)

    return app
