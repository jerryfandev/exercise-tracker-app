from flask import abort, request, jsonify, render_template, session, redirect, url_for, flash, current_app
from .models import db, User, ExerciseLog, Achievement, FriendRequest
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from flask_login import login_user
from flask_login import current_user
from .forms import LoginForm, RegistrationForm


def handle_login():  # Handles user login
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Check if the user is a normal user
            user = User.query.filter((User.username == username) | (User.email == username)).first()

            if user and user.check_password(password):
                if not user.is_active:
                    return jsonify(success=False, message="Account is disabled. Please contact support.")

                # Update the last login timestamp
                user.last_login = datetime.utcnow()

                try:
                    db.session.commit()

                    # Set the session
                    session['user_id'] = user.id
                    login_user(user)

                    return jsonify(success=True, redirect='/dashboard')
                except Exception as e:
                    db.session.rollback()
                    return jsonify(success=False, message="Login failed: " + str(e))
            else:
                return jsonify(success=False, message="Invalid username or password")
        else:
            errors = {field.name: field.errors for field in form if field.errors}
            return jsonify(success=False, message="Validation failed", errors=errors)

    return render_template('login.html', form=form)


def handle_register():  # Handles user registration
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            phone = form.phone.data.strip() if form.phone.data else None

            # Create new user
            new_user = User(
                username=username,
                email=email,
                phone=phone
            )
            new_user.set_password(password)

            try:
                db.session.add(new_user)
                db.session.commit()
                return jsonify(success=True)
            except Exception as e:
                db.session.rollback()
                return jsonify(success=False, message="Registration failed: " + str(e))
        else:
            # Handle form validation errors.
            errors = {}
            for field_name, field_errors in form.errors.items():
                errors[field_name] = field_errors

            # 
            if 'username' in errors and any('already exists' in err.lower() for err in errors['username']):
                return jsonify(success=False, message="User has already existed, please choose another username.",
                               errors=errors)

            return jsonify(success=False, message="Validation failed", errors=errors)

    return render_template('register.html', form=form)


# This function checks if the user is an admin.
def is_admin(username, password):
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')  # Default to 'admin' if not set in environment variables
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin')
    return username == admin_username and password == admin_password


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

        return render_template(
            'dashboard.html',
            total_exercises=total_exercises,
            last_calories=last_calories
        )
    return render_template('login.html')


def connect_db_to_charts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_id = user.id

    today = datetime.utcnow().date()
    past_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    logs = ExerciseLog.query.filter(
        ExerciseLog.user_id == user_id,
        ExerciseLog.date >= past_7_days[0]
    ).all()

    cal_per_day = {day: 0 for day in past_7_days}
    duration_per_day = {day: 0 for day in past_7_days}

    for log in logs:
        log_day = log.date.date()
        if log_day in cal_per_day:
            cal_per_day[log_day] += log.calories
            duration_per_day[log_day] += log.duration

    p7d_labels = [day.strftime('%a') for day in past_7_days]
    p7d_cal = [cal_per_day[day] for day in past_7_days]

    bubble_data = []
    for i, day in enumerate(past_7_days):
        minutes = duration_per_day[day]
        bubble_data.append({
            'x': i + 1,
            'y': minutes,
            'r': min(30, max(3, minutes / 5))
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
    achievements = get_achievements(session['user_id'])

    # Add icon for each exercise type
    for achievement in achievements:
        match achievement.exercise_type.lower():
            case 'all':
                achievement.icon = '⭐'
            case 'running':
                achievement.icon = '🏃'
            case 'cycling':
                achievement.icon = '🚴'
            case 'swimming':
                achievement.icon = '🏊'
            case 'yoga':
                achievement.icon = '🧘'
            case _:
                achievement.icon = '🧩'

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
    return render_template('profile.html', achievements=achievements)


def view_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template('view-profile.html')
    if current_user.is_authenticated and user.id == current_user.id:
        return redirect(url_for('profile'))
    achievements = get_achievements(user.id)

    # Add icon for each exercise type
    for achievement in achievements:
        match achievement.exercise_type.lower():
            case 'all':
                achievement.icon = '⭐'
            case 'running':
                achievement.icon = '🏃'
            case 'cycling':
                achievement.icon = '🚴'
            case 'swimming':
                achievement.icon = '🏊'
            case 'yoga':
                achievement.icon = '🧘'
            case _:
                achievement.icon = '🧩'
    return render_template('view-profile.html', profile_user=user, achievements=achievements)


def init_sharing():
    users = User.query.filter(User.id != current_user.id).all()
    friend_ids = {friend.id for friend in current_user.friends()}
    shared_data = [
        {
            'username': f.username,
            'email': f.email,
            'is_friend': f.id in friend_ids,
            'sent': current_user.has_pending_request_to(f),
            'approval': current_user.has_pending_request_from(f),
            'avatar_path': f.avatar_path or 'asset/avatar.png'
        }
        for f in users
    ]
    return render_template('sharing.html', shared_data=shared_data)


def handle_exercise_log():
    # Ensure the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        # Validate CSRF token (Flask-WTF handles this automatically)
        exercise_type = request.form['exercise_type']
        duration = int(request.form['duration'])
        calories = int(request.form['calories'])

        log = ExerciseLog(user_id=user_id, exercise_type=exercise_type, duration=duration, calories=calories)
        db.session.add(log)
        db.session.commit()

        # achievement for each type
        thresholds = range(500, 5001, 500)
        sum_type_duration = db.session.query(db.func.sum(ExerciseLog.duration)) \
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
        sum_all_duration = db.session.query(db.func.sum(ExerciseLog.duration)) \
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
    achievements = Achievement.query.filter_by(user_id=user_id) \
        .order_by(Achievement.achieved_at.desc()).all()
    return render_template('achievement.html', achievements=achievements)


def handle_add_friend(user_id):
    target_user = User.query.get_or_404(user_id)

    if current_user.id == user_id:
        flash("You can't send a friend request to yourself.", 'warning')
    elif current_user.has_pending_request_to(target_user):
        flash("Friend request already sent.", 'info')
    elif current_user.has_pending_request_from(target_user):
        request = FriendRequest.query.filter_by(sender_id=user_id, receiver_id=current_user.id,
                                                status='pending').first()
        request.status = 'accepted'
        db.session.commit()
        flash("Friend request accepted automatically!", 'success')
    elif current_user.is_friend_with(target_user):
        flash("You are already friends.", 'info')
    else:
        fr = FriendRequest(sender_id=current_user.id, receiver_id=user_id)
        db.session.add(fr)
        db.session.commit()
        flash("Friend request sent!", 'success')

    return redirect(url_for('view_others', username=target_user.username))


def handle_respond_request(user_id, response):
    fr = FriendRequest.query.filter_by(sender_id=user_id, receiver_id=current_user.id,
                                       status='pending').first_or_404()
    sender_user = User.query.get_or_404(user_id)
    if response == 'accept':
        fr.status = 'accepted'
        flash("Friend request accepted!", 'success')
    elif response == 'deny':
        fr.status = 'denied'
        flash("Friend request denied.", 'info')

    db.session.commit()
    return redirect(url_for('view_others', username=sender_user.username))


def get_achievements(user_id):
    return Achievement.query.filter_by(user_id=user_id) \
        .order_by(Achievement.achieved_at.desc()).all()
