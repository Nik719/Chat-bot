import logging
from flask import current_app, jsonify
import json
import requests
import re
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.services.phi_service import PhiService

# Configure logger
logger = logging.getLogger(__name__)

# Initialize global phi_service
phi_service = None


def get_phi_service():
    global phi_service
    if phi_service is None:
        phi_service = PhiService()
    return phi_service


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


# def generate_response(response):
#     # Return text in uppercase
#     return response.upper()


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    """
    Process incoming WhatsApp messages and generate responses using Phi.
    
    Args:
        body (dict): The incoming webhook payload from WhatsApp
        
    Returns:
        dict: Response to be sent back to the webhook
    """
    # Check if it's a valid WhatsApp message
    if not is_valid_whatsapp_message(body):
        return {"statusCode": 404, "body": "Not a valid WhatsApp message"}

    try:
        # Extract message details
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
        message_body = message["text"]["body"]
        from_number = message["from"]
        
        # Get user's profile name (fallback to 'User' if not available)
        name = "User"
        try:
            profile_name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
            if profile_name and profile_name.strip():
                name = profile_name
        except (KeyError, IndexError, TypeError):
            pass  # Use default name if profile name not available
        
        # Log the incoming message
        logger.info(f"Received message from {name} ({from_number}): {message_body}")
        
        # Get response from Phi
        phi_service = get_phi_service()
        response = phi_service.generate_response(message_body, from_number, name)
        
        if not response:
            response = "I'm sorry, I couldn't process your request at the moment. Please try again later."
        
        # Process the response for WhatsApp formatting
        processed_response = process_text_for_whatsapp(response)
        
        # Send the response back to WhatsApp
        data = get_text_message_input(from_number, processed_response)
        send_message(data)
        
        return {"statusCode": 200, "body": "Message processed successfully"}
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        return {"statusCode": 500, "body": "Error processing message"}


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
