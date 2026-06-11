import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Define the database path
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gminsta.db')

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows dictionary-like access to rows
    return conn

def init_db():
    """Initializes the database with necessary tables if they don't exist."""
    conn = get_db_connection()
    
    # Create Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create Posts table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create Likes table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
            UNIQUE(user_id, post_id)
        )
    ''')
    
    # Create Comments table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(name, email, password):
    """Creates a new user with a hashed password."""
    conn = get_db_connection()
    hashed_password = generate_password_hash(password)
    try:
        conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                     (name, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # User with this email already exists
    finally:
        conn.close()

def get_user_by_email(email):
    """Retrieves a user by their email address."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Retrieves a user by their ID."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def verify_user(email, password):
    """Verifies a user's credentials."""
    user = get_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        return user
    return None

def create_post(user_id, content):
    """Creates a new post for a user."""
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (user_id, content))
    conn.commit()
    conn.close()

def _attach_post_data(conn, posts, current_user_id=None):
    """Helper to attach likes and comments to a list of posts."""
    enriched_posts = []
    for post in posts:
        post_dict = dict(post)
        
        # Get like count
        like_count = conn.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (post['id'],)).fetchone()[0]
        post_dict['like_count'] = like_count
        
        # Check if current user liked it
        post_dict['has_liked'] = False
        if current_user_id:
            like = conn.execute('SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?', (current_user_id, post['id'])).fetchone()
            if like:
                post_dict['has_liked'] = True
                
        # Get comments
        comments = conn.execute('''
            SELECT c.id, c.content, c.created_at, u.name as author_name
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        ''', (post['id'],)).fetchall()
        post_dict['comments'] = [dict(c) for c in comments]
        
        enriched_posts.append(post_dict)
    return enriched_posts

def get_all_posts(current_user_id=None):
    """Retrieves all posts with the associated user's name, likes, and comments."""
    conn = get_db_connection()
    # Join posts and users to get the author's name
    posts = conn.execute('''
        SELECT p.id, p.content, p.created_at, u.name as author_name, u.id as author_id
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    ''').fetchall()
    enriched_posts = _attach_post_data(conn, posts, current_user_id)
    conn.close()
    return enriched_posts

def get_user_posts(user_id, current_user_id=None):
    """Retrieves all posts for a specific user, with likes and comments."""
    conn = get_db_connection()
    posts = conn.execute('''
        SELECT p.id, p.content, p.created_at, u.name as author_name, u.id as author_id
        FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.user_id = ?
        ORDER BY p.created_at DESC
    ''', (user_id,)).fetchall()
    enriched_posts = _attach_post_data(conn, posts, current_user_id)
    conn.close()
    return enriched_posts

def delete_post(post_id, user_id):
    """Deletes a post if the user_id matches the post's author."""
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ? AND user_id = ?', (post_id, user_id))
    conn.commit()
    conn.close()

def toggle_like(user_id, post_id):
    """Toggles a like for a specific post by a user."""
    conn = get_db_connection()
    like = conn.execute('SELECT * FROM likes WHERE user_id = ? AND post_id = ?', (user_id, post_id)).fetchone()
    if like:
        conn.execute('DELETE FROM likes WHERE user_id = ? AND post_id = ?', (user_id, post_id))
    else:
        conn.execute('INSERT INTO likes (user_id, post_id) VALUES (?, ?)', (user_id, post_id))
    conn.commit()
    conn.close()

def add_comment(user_id, post_id, content):
    """Adds a comment to a specific post."""
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (user_id, post_id, content) VALUES (?, ?, ?)', (user_id, post_id, content))
    conn.commit()
    conn.close()
