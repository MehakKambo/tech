from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def create_account(email, first_name, type, status, password1):
    new_user = User(email=email, first_name=first_name, account_type=type, status=status, password=generate_password_hash(
        password1, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)
    flash('Account created!', category='success')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        status = 'pending'
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 7 characters.', category='error')
        elif request.form.get('studentCheckbox') == 'True':
            if not email.endswith('@uw.edu'):
                flash('Invalid email domain. You must use an email ending with @uw.edu', category='error')
            else:
                #create student account
                status = "active" #student accounts are automatically active
                create_account(email, first_name, 'student', status, password1)
                return redirect(url_for('views.home'))
        else:
            #create mentor
            create_account(email, first_name, 'mentor', status, password1)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

#takes in a user id and changes the account type from student to mentor or vice versa
@auth.route('/change-account-type', methods=['POST'])
@login_required
def change_account_type():
    data = request.get_json()
    id = data.get('userId')
    newType = data.get('newType')
    
    user = User.query.get_or_404(id)
    user.account_type = newType
    db.session.commit()

    return jsonify(success=True)

@auth.route('/change-account-status', methods=['POST'])
@login_required
def change_account_status():
    data = request.get_json()
    id = data.get('userId')
    newStatus = data.get('newStatus')
    
    user = User.query.get_or_404(id)
    user.status = newStatus
    db.session.commit()

    return jsonify(success=True)

