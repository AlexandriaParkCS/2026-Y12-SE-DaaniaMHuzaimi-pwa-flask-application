import re
from functools import wraps
from flask import (Blueprint, render_template, redirect, url_for, session, flash, request)
from models.user import User
from database import db
from forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__)

def sanitise(text):
    # Strip HTML tags - prevents XSS attacks
    return re.sub(r'<[^>]+>', '', str(text)).strip()

def login_required(f):
    @wraps(f)
    def decorated(*args, ** kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, ** kwargs)
    return decorated

@auth_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('sleep.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods= ['GET' , 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = sanitise(form.username.data)
        email = sanitise(form.email.data.lower())
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html', form=form)
        if User.query.filter_by(username=username).first():
            flash('Username taken.', 'danger')
            return render_template('register.html', form=form)
        user = User(username=username, email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST' ])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = sanitise(form.email.data.lower())
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('sleep.dashboard'))
        flash('incorrect email or password.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Signed out.', 'info')
    return redirect(url_for('auth.login'))
@auth_bp.route('/delete-account', methods =['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    if user:
        db.session.delete(user)
        db.session.commit()
    session.clear()
    flash('Account deleted.', 'info')
    return redirect(url_for('auth.login'))
                                
          