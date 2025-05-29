import os
import logging
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('phi_service.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class PhiService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PhiService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.endpoint = os.getenv("ENDPOINT_URL")
            self.api_key = os.getenv("PHI_API_KEY")
            self.deployment = os.getenv("DEPLOYMENT_NAME")
            
            if not all([self.endpoint, self.api_key, self.deployment]):
                raise ValueError("Missing required environment variables for Phi service")
            
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "api-version": "2025-01-01-preview"
            }
            self.initialized = True

    def generate_response(self, message_body: str, wa_id: str, name: str) -> str:
        """
        Generate a response using Phi chat completion.
        
        Args:
            message_body (str): The message content from the user
            wa_id (str): WhatsApp ID of the user
            name (str): Name of the user
            
        Returns:
            str: The AI's response or None if there was an error
        """
        try:
            if not message_body or not message_body.strip():
                logger.warning(f"Empty message body received from {name} ({wa_id})")
                return "I received an empty message. Please type something and try again."
                
            logger.info(f"Generating response for {name} ({wa_id}): {message_body[:100]}...")
            
            # Prepare the request payload
            payload = {
                "model": self.deployment,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            f"You are a helpful and friendly assistant talking to {name} on WhatsApp. "
                            "Keep responses concise, natural, and conversational. "
                            "Use emojis occasionally to make the conversation more engaging. "
                            "If you don't know something, be honest about it."
                        )
                    },
                    {"role": "user", "content": message_body}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            # Make the API request with timeout and better error handling
            try:
                logger.info(f"Sending request to Phi API endpoint: {self.endpoint}")
                response = requests.post(
                    self.endpoint,
                    headers=self.headers,
                    json=payload,
                    timeout=60  # 60 seconds timeout
                )
                
                # Log response status and headers for debugging
                logger.info(f"Response status code: {response.status_code}")
                logger.debug(f"Response headers: {response.headers}")
                
                # Check for HTTP errors
                response.raise_for_status()
                
                # Parse JSON response
                response_data = response.json()
                logger.debug(f"Response data: {response_data}")
                
                # Extract the response content
                if response_data and "choices" in response_data and len(response_data["choices"]) > 0:
                    # Handle both response formats:
                    # 1. Direct content in the choice
                    # 2. Content in a message object within the choice
                    choice = response_data["choices"][0]
                    if "text" in choice:
                        ai_response = choice["text"].strip()
                    elif "message" in choice and "content" in choice["message"]:
                        ai_response = choice["message"]["content"].strip()
                    else:
                        # Fallback to the first key that might contain the response
                        for key in ["text", "content", "response"]:
                            if key in choice:
                                ai_response = str(choice[key]).strip()
                                break
                        else:
                            ai_response = str(choice).strip()
                    
                    if not ai_response:
                        logger.warning(f"Received empty response from Phi for user {name} ({wa_id})")
                        return "I'm not sure how to respond to that. Could you please rephrase or ask something else?"
                    return ai_response
                    
                logger.warning(f"Unexpected response format from Phi for user {name} ({wa_id})")
                return "I received an unexpected response. Could you please try again?"
                
            except requests.exceptions.Timeout:
                logger.error(f"Request to Phi API timed out for user {name} ({wa_id})")
                return "The AI service is taking too long to respond. Please try again in a moment."
                
            except requests.exceptions.HTTPError as http_err:
                logger.error(f"HTTP error occurred for user {name} ({wa_id}): {http_err}")
                logger.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
                return "There was an error processing your request. Please try again later."
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error in generate_response for {name} ({wa_id}): {str(e)}")
                return "I'm having trouble connecting to the AI service. Please try again later."
            
            except Exception as e:
                logger.error(f"Unexpected error in generate_response for {name} ({wa_id}): {str(e)}", exc_info=True)
                return "An unexpected error occurred. Please try again later."
        except Exception as e:
            logger.error(f"Error in generate_response for {name} ({wa_id}): {str(e)}", exc_info=True)
            return "Sorry, I encountered an error while processing your request. Please try again later."
