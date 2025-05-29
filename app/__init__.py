from flask import Flask
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure app
    app.config.update(
        ACCESS_TOKEN=os.getenv('ACCESS_TOKEN'),
        VERSION=os.getenv('VERSION'),
        PHONE_NUMBER_ID=os.getenv('PHONE_NUMBER_ID'),
        RECIPIENT_WAID=os.getenv('RECIPIENT_WAID'),
        APP_SECRET=os.getenv("APP_SECRET")
    )

    if not app.config["APP_SECRET"]:
        raise ValueError("APP_SECRET environment variable is not set")

    # Register blueprints
    from .views import webhook_blueprint
    app.register_blueprint(webhook_blueprint)

    logger.info("Flask app created and configured")
    return app
