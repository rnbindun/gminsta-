from flask import Flask
from database import db
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.user import user_bp
import secrets

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Generate a secret key for session management
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    
    # Initialize the database
    with app.app_context():
        db.init_db()
        
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(user_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Run the application in debug mode for development
    app.run(debug=True)
