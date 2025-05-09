from flask import request, jsonify, render_template, session, redirect, url_for, flash, current_app
from .models import db, User, ExerciseLog, Achievement
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os


def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return jsonify(success=True)
        
        # For backward compatibility, check admin hardcoded credentials
        admin = is_admin(username, password)
        if admin:
            return jsonify(success=True, is_admin=True)
            
        return jsonify(success=False)
    
    return render_template('login.html')


def handle_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone')  # Add this 'phone' field to the User model and database table.
        
        # Check if username, email or phone already exists
        existing_user = User.query.filter(
            (User.username == username) | 
            (User.email == email) |
            (User.phone == phone)  # Add this test to check if the phone number already exists.  
        ).first()
            
        if existing_user:
            if existing_user.username == username:
                return jsonify(success=False, message="Username already exists")
            elif existing_user.email == email:
                return jsonify(success=False, message="Email already exists")
            elif existing_user.phone == phone:
                return jsonify(success=False, message="Phone number already exists")
        
        # Create new user
        new_user = User(
            username=username, 
            email=email,
            phone=phone  # Add this 'phone' field to the User model and database table.
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify(success=True)
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, message="Registration failed: " + str(e))
    
    return render_template('register.html')


# This function checks if the user is an admin.
def is_admin(username, password):
    return username == "admin" and password == "admin"


# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def init_dashboard():
    if request.method == 'GET':
        user_id = session['user_id']

        total_exercises = ExerciseLog.query.filter_by(user_id=user_id).count()

        latest_exercise = ExerciseLog.query.filter_by(user_id=user_id).order_by(ExerciseLog.date.desc()).first()
        last_calories = latest_exercise.calories if latest_exercise else 0
        return render_template('dashboard.html', total_exercises=total_exercises, last_calories=last_calories)
    return render_template('login.html')

def connect_db_to_charts():
    user_id = session['user_id']

    today = datetime.utcnow().date()
    past_7_days = [today - timedelta(days = i) for i in range(6,-1,-1)]
    past_100_days = [today - timedelta(days = i) for i in range(99,-1,-1)]

    p7d_logs = ExerciseLog.query.filter(ExerciseLog.user_id == user_id, ExerciseLog.date >= past_7_days[0]).all()
    p100d_logs = ExerciseLog.query.filter(ExerciseLog.user_id == user_id, ExerciseLog.date >= past_100_days[0]).all()

    cal_per_day = {day: 0 for day in past_7_days}
    duration_per_day = {day: 0 for day in past_100_days}

    for log in p7d_logs:
        log_day = log.date.date()
        if log_day in cal_per_day:
            cal_per_day[log_day] += log.calories

    for log in p100d_logs:
        log_day = log.date.date()
        if log_day in duration_per_day:
            duration_per_day[log_day] += log.duration

    p7d_labels = [day.strftime('%a') for day in past_7_days]
    p7d_cal = [cal_per_day[day] for day in past_7_days]

    bubble_data = []
    for i, day in enumerate(past_100_days):
        minutes = duration_per_day[day]
        bubble_data.append({
            'x': i + 1,
            'y': minutes,
            'r': min(30, max(3, minutes / 15))
        })

    return jsonify({'p7d_labels': p7d_labels, 'p7d_cal': p7d_cal, 'bubble_data': bubble_data})


def init_profile():
    # Debug: Check method
    print("METHOD:", request.method)

    # Ensure the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get the current user from the session
    user = User.query.get(session['user_id'])
    
    # Handle profile update when the form is submitted (POST method)
    if request.method == 'POST':
        current_password = request.form.get('current_password')

        # Check if current password is provided
        if not current_password:
            flash('Current password is required to update profile.', 'danger')
            return redirect(url_for('profile'))

        # Verify if the provided password matches the stored password
        if not user.check_password(current_password):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('profile'))

        # Debug: Check form data
        print("Form Data Received:")
        print(f"New Username: {request.form.get('username')}")
        print(f"New Email: {request.form.get('email')}")
        print(f"New Full Name: {request.form.get('full_name')}")
        print(f"New DOB: {request.form.get('dob')}")
        print(f"New Gender: {request.form.get('gender')}")
        print(f"New Height: {request.form.get('height_cm')}")
        print(f"New Weight: {request.form.get('weight_kg')}")
        print(f"New Avatar: {request.files.get('profile_image')}")

        # Process form data and update user fields if new data is provided
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_full_name = request.form.get('full_name')
        new_dob = request.form.get('dob')
        new_gender = request.form.get('gender')
        new_height_cm = request.form.get('height_cm')
        new_weight_kg = request.form.get('weight_kg')
        new_profile_image = request.files.get('profile_image')

        # Profile image
        if new_profile_image and new_profile_image.filename != '':
            upload_folder = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)  # Tạo thư mục nếu chưa có

            # Delete current avatar if it exists
            if user.avatar_path and user.avatar_path != 'asset/avatar.png':
                old_path = os.path.join(current_app.static_folder, user.avatar_path)
                if os.path.exists(old_path):
                    os.remove(old_path)
    
            # Save the new profile image
            filename = secure_filename(new_profile_image.filename)
            new_path = os.path.join(upload_folder, filename)
            new_profile_image.save(new_path)
            user.avatar_path = f'uploads/{filename}'


        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_full_name:
            user.full_name = new_full_name
        if new_dob:
            try:
                user.dob = datetime.strptime(new_dob, '%Y-%m-%d').date()  # Update DOB if valid
            except ValueError:
                flash('Invalid DOB format. Please enter in YYYY-MM-DD format.', 'danger')
                return redirect(url_for('profile'))
        if new_gender:
            user.gender = new_gender
        if new_height_cm:
            try:
                user.height_cm = float(new_height_cm)  # Convert height to float
            except ValueError:
                flash('Invalid height format. Please enter a valid number.', 'danger')
                return redirect(url_for('profile'))
        if new_weight_kg:
            try:
                user.weight_kg = float(new_weight_kg)  # Convert weight to float
            except ValueError:
                flash('Invalid weight format. Please enter a valid number.', 'danger')
                return redirect(url_for('profile'))

        # Commit the changes to the database
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))  # Redirect to profile page to see updated data
        except Exception as e:
            print(f"Error during commit: {e}")  # Debugging: Print the error
            db.session.rollback()
            flash('Profile update failed. Please try again later.', 'danger')
            return redirect(url_for('profile'))

    # If GET request, just render the profile page with the user's current data
    return render_template('profile.html')


def init_sharing():
    if request.method == 'GET':
        # TODO
        # Dummy data for shared datasets
        shared_data = [
            {
                'title': f'Dataset {i+1}',
                'user_name': f'User {i+1}',
                'user_email': f'user{i+1}@example.com',
                'shared_date': datetime(2024, 4, (i % 30) + 1).strftime('%d/%m/%Y')
            }
            for i in range(20)
        ]
        return render_template('sharing.html', shared_data = shared_data)
    return render_template('login.html')


def handle_exercise_log():
    user_id = session['user_id']

    if request.method == 'POST':
        exercise_type = request.form['exercise_type']
        duration = int(request.form['duration'])
        calories = int(request.form['calories'])

        log = ExerciseLog(user_id=user_id, exercise_type=exercise_type, duration=duration, calories=calories)
        db.session.add(log)
        db.session.commit()

        # achievement for each type
        thresholds = range(500, 5001, 500)
        sum_type_duration = db.session.query(db.func.sum(ExerciseLog.duration))\
            .filter_by(user_id=user_id, exercise_type=exercise_type).scalar() or 0

        for threshold in thresholds:
            # check if the achievement already exists
            existing = Achievement.query.filter_by(
                user_id=user_id,
                exercise_type=exercise_type,
                description=f"Accumulate {threshold} minutes of {exercise_type}!"
            ).first()

            if sum_type_duration >= threshold and not existing:
                achievement = Achievement(
                    user_id=user_id,
                    exercise_type=exercise_type,
                    description=f"Accumulate {threshold} minutes of {exercise_type}!"
                )
                db.session.add(achievement)

        # achievement for all types
        # calculate the total duration for all exercise types
        # check if the achievement already exists
        sum_all_duration = db.session.query(db.func.sum(ExerciseLog.duration))\
            .filter_by(user_id=user_id).scalar() or 0

        for threshold in thresholds:
            existing_all = Achievement.query.filter_by(
                user_id=user_id,
                exercise_type='ALL',
                description=f"Accumulate {threshold} total minutes of all exercise types!"
            ).first()

            if sum_all_duration >= threshold and not existing_all:
                achievement = Achievement(
                    user_id=user_id,
                    exercise_type='ALL',
                    description=f"Accumulate {threshold} total minutes of all exercise types!"
                )
                db.session.add(achievement)

        db.session.commit()
        return redirect(url_for('exercise_log'))

    logs = ExerciseLog.query.filter_by(user_id=user_id).order_by(ExerciseLog.date.desc()).all()
    return render_template('exercise_log.html', logs=logs)


def handle_achievement():
        user_id = session['user_id']
        achievements = Achievement.query.filter_by(user_id=user_id)\
            .order_by(Achievement.achieved_at.desc()).all()
        return render_template('achievement.html', achievements=achievements)
