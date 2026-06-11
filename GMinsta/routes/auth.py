from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db

# Create the auth blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to feed
    if 'user_id' in session:
        return redirect(url_for('posts.feed'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Basic validation
        if not name or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('auth.register'))
            
        # Attempt to create the user in the database
        success = db.create_user(name, email, password)
        
        if success:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email already registered!', 'error')
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to feed
    if 'user_id' in session:
        return redirect(url_for('posts.feed'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verify user credentials
        user = db.verify_user(email, password)
        
        if user:
            # Create session for the user
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('posts.feed'))
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
