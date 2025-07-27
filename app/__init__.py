from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Set your secret key here

    # Configure upload and result folders
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['RESULT_FOLDER'] = os.path.join(app.root_path, 'static', 'results')

    # Ensure folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.analyze import analyze_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(analyze_bp)

    return app