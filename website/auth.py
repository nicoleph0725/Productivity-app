from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


authentication = Blueprint('auth', __name__)

@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # filter all the emails with the specific email inputted
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # starts user session
                return redirect(url_for('main_views.home'))
            else:
                flash('Incorrect password, try again')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)


@authentication.route('/logout')
@login_required # can't access this if a user isn't logged in
def logout():
    logout_user() # ends user session
    return redirect(url_for('auth.login'))


@authentication.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
       email = request.form.get('email')
       nickname = request.form.get('nickname')
       password1 = request.form.get('password1')
       password2 = request.form.get('password2')

       new_user = User.query.filter_by(email=email).first()
       if new_user:
           flash('Email already exists', category='error')
       if len(email) < 4:
           flash('Email is too short', category='error')

       elif len(nickname) < 2:
           flash('Nickname must be greater than 1 characters', category='error')

       elif password1 != password2:
           flash('Passwords don\'t match', category='error')

       elif len(password1) < 7:
           flash('Password must be at least 7 characters', category='error')
       else:
           new_user = User(email=email, nickname=nickname, password=generate_password_hash(password1))
           db.session.add(new_user)
           db.session.commit()
           login_user(new_user, remember=True)
           flash('Account created!', category='success')
           return redirect(url_for('main_views.home'))

    return render_template("sign_up.html", user=current_user)

