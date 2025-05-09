from flask import session, redirect, url_for
from .functions import *

# This file contains the routes for the Flask application.
def register_routes(app):
    # The home route renders the index.html template.
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return handle_login()

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        return handle_register()

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return init_dashboard()

    @app.route('/charts')
    @login_required
    def charts():
        return connect_db_to_charts()
    

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        return init_profile()

    @app.route('/sharing', methods=['GET', 'POST'])
    @login_required
    def sharing():
        return init_sharing()
        
    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('home'))
    

    @app.route('/exercise_log', methods=['GET', 'POST'])
    @login_required
    def exercise_log():
        return handle_exercise_log()
    
    @app.route('/achievement')
    @login_required
    def achievement():
        return handle_achievement()
    