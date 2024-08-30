from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object('config.Config')

    # Ensure the folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
