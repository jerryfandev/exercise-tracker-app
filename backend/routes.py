from flask import session, redirect, url_for, render_template, request, jsonify, flash, current_app
from .models import db, User, ExerciseLog, Achievement, FriendRequest
from .functions import login_required, handle_login, handle_register, init_dashboard, connect_db_to_charts
from .functions import init_profile, view_profile, init_sharing, handle_exercise_log, handle_achievement, handle_add_friend
from flask_login import current_user
from .blueprints import main

# All routes now use main blueprint instead of app

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    return handle_login()

@main.route('/register', methods=['GET', 'POST'])
def register():
    return handle_register()

@main.route('/dashboard')
@login_required
def dashboard():
    return init_dashboard()

@main.route('/charts')
@login_required
def charts():
    username = request.args.get('username') or current_user.username
    return connect_db_to_charts(username)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return init_profile()

@main.route('/profile/<username>', methods=['GET'])
@login_required
def view_others(username):
    if username == current_user.username:
        return redirect(url_for('main.profile'))
    return view_profile(username)

@main.route('/sharing', methods=['GET', 'POST'])
@login_required
def sharing():
    return init_sharing()

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.home'))

@main.route('/exercise_log', methods=['GET', 'POST'])
@login_required
def exercise_log():
    return handle_exercise_log()

@main.route('/achievement')
@login_required
def achievement():
    return handle_achievement()

@main.route('/add_friend/<int:user_id>', methods=['POST'])
@login_required
def add_friend(user_id):
    return handle_add_friend(user_id)

@main.route('/remove_friend', methods=['POST'])
@login_required
def remove_friend():
    user_id = request.form.get('user_id')
    return redirect(url_for('main.sharing'))

@main.route('/cancel_request', methods=['POST'])
@login_required
def cancel_request():
    user_id = request.form.get('user_id')
    return redirect(url_for('main.sharing'))

@main.route('/respond_request/<int:user_id>/<response>', methods=['POST'])
@login_required
def respond_request(user_id, response):
    return redirect(url_for('main.sharing'))

# The function to register routes is no longer needed as we register the blueprint directly in __init__.py
def register_routes(app):
    # This function can be left empty or removed
    pass
