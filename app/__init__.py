import os
from flask import Flask
from .extensions import db

def create_app():
    app = Flask(__name__)
    
    # Configure the application
    app.config.from_pyfile('../config.py')
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"Instance path: {app.instance_path}")
    except OSError as e:
        print(f"Error creating instance folder: {e}")

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from .imports.routes import import_bp
    app.register_blueprint(import_bp, url_prefix='/import')

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")
            # Provide more detailed error information
            import traceback
            traceback.print_exc()
            
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app