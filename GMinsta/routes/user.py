from flask import Blueprint, render_template, redirect, url_for, session, flash
from database import db

# Create the user blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
def profile():
    # Ensure user is logged in
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'info')
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    user = db.get_user_by_id(user_id)
    user_posts = db.get_user_posts(user_id, current_user_id=session['user_id'])
    
    return render_template('profile.html', user=user, posts=user_posts)

@user_bp.route('/chat')
def chat():
    # Ensure user is logged in
    if 'user_id' not in session:
        flash('Please log in to access chat.', 'info')
        return redirect(url_for('auth.login'))
        
    # Render the chat UI
    return render_template('chat.html')
