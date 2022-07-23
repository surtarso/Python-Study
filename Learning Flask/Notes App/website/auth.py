from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user

#define as a blueprint (kinda like urls.py from django)
auth = Blueprint('auth', __name__)


##-----------------------------------------------------LOGIN:
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        #filter users with this email
        user = User.query.filter_by(email=email).first()
        
        if user:
            #success:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.notes'))
            #error check:
            else:
                flash('Incorrect credentials', category='error')
        else:
            flash('Email doesnt exist', category='error')
        
    return render_template('login.html', user=current_user)


##----------------------------------------------------LOGOUT:
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


##----------------------------------------------------REGISTER:
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()

        #errorcheck:
        if user:
            flash('email already used', category='error')
        elif len(email) < 4:
            flash('invalid email', category='error')
        elif len(firstName) < 2:
            flash('invalid name', category='error')
        elif len(lastName) < 2:
            flash('invalid name', category='error')
        elif len(password1) < 7:
            flash('invalid password', category='error')
        elif password2 != password1:
            flash('passwords dont match', category='error')
        #sucess:
        else:
            newUser = User(email=email, firstName=firstName, lastName=lastName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(newUser)
            db.session.commit()
            flash('account created', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.notes'))
        
    return render_template('sign_up.html', user=current_user)