from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists.', 'error')
            return redirect(url_for('auth.register'))
            
        new_user = User(email=email, name=name, password_hash=generate_password_hash(password))
        
        db.session.add(new_user)
        db.session.commit()
        
        # Seed default categories for this user
        from models import Category
        default_categories = [
            {'name': 'Food', 'type': 'expense'},
            {'name': 'Transport', 'type': 'expense'},
            {'name': 'Shopping', 'type': 'expense'},
            {'name': 'Bills', 'type': 'expense'},
            {'name': 'Health', 'type': 'expense'},
            {'name': 'Education', 'type': 'expense'},
            {'name': 'Entertainment', 'type': 'expense'},
            {'name': 'Salary', 'type': 'income'}
        ]
        for cat in default_categories:
            db.session.add(Category(user_id=new_user.id, name=cat['name'], type=cat['type']))
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=remember)
        return redirect(url_for('main.dashboard'))
        
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
