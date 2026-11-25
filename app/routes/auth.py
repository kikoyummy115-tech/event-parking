from flask import Blueprint, request, url_for, redirect, flash, render_template
from flask_login import login_user, logout_user, login_required
from extension import db
from app.models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip() 
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        if not username or not email or not password:
            flash('Please fill out all fields', 'danger')
            return render_template('auth/register.html')

        if len(password) < 8:
            flash('Password be at least 8 character', 'warning')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already Exist', 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = User(
            username=username,
            email=email,
            role="user"
        )
        new_user.password = password
        try:
            db.session.add(new_user)
            db.session.commit()
            print("Register successful")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print("Error Could not create new account", e)
        
    return render_template("auth/register.html")


@auth.route("/login", methods=['GET', "POST"])
def login():
    "Login in user required username and password"

    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        user = User.query.filter_by(email=email).first()
        
        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.get_events'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('auth/login.html')


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():    
    logout_user()
    flash("Successfully logout account", 'success')
    return redirect(url_for('auth.login'))