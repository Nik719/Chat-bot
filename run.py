from app import create_app
from app.services.phi_service import PhiService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = create_app()

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000, debug=True)