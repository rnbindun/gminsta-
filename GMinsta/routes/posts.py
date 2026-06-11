from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db

# Create the posts blueprint
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/')
@posts_bp.route('/feed')
def feed():
    # Ensure user is logged in
    if 'user_id' not in session:
        flash('Please log in to view the feed.', 'info')
        return redirect(url_for('auth.login'))
        
    # Get all posts for the feed with like and comment data
    all_posts = db.get_all_posts(current_user_id=session['user_id'])
    return render_template('feed.html', posts=all_posts)

@posts_bp.route('/create_post', methods=['POST'])
def create_post():
    # Ensure user is logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    content = request.form.get('content')
    
    if not content:
        flash('Post content cannot be empty!', 'error')
    else:
        # Save post to database
        db.create_post(session['user_id'], content)
        flash('Post created successfully!', 'success')
        
    return redirect(url_for('posts.feed'))

@posts_bp.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # Ensure user is logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    # Attempt to delete the post (the db function checks ownership implicitly)
    db.delete_post(post_id, session['user_id'])
    flash('Post deleted!', 'success')
    
    # Redirect back to where the request came from (feed or profile)
    return redirect(request.referrer or url_for('posts.feed'))

@posts_bp.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    db.toggle_like(session['user_id'], post_id)
    return redirect(request.referrer or url_for('posts.feed'))

@posts_bp.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    content = request.form.get('content')
    if content:
        db.add_comment(session['user_id'], post_id, content)
    else:
        flash('Comment cannot be empty.', 'error')
        
    return redirect(request.referrer or url_for('posts.feed'))
