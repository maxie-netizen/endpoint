from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt
from models import User

# Define the blueprint HERE
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. Please login.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
