# from openai import AzureOpenAI
# from typing import Dict, Any
# import logging
# import os
# from dotenv import load_dotenv

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables from .env file``
# load_dotenv()

# class AzuraService:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(AzuraService, cls).__new__(cls)
#         return cls._instance

#     def __init__(self):
#         if not hasattr(self, 'initialized'):
#             self.endpoint = os.getenv("ENDPOINT_URL")
#             self.deployment = os.getenv("DEPLOYMENT_NAME")
#             self.subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
            
#             if not all([self.endpoint, self.deployment, self.subscription_key]):
#                 raise ValueError("Missing required environment variables")
            
#             try:
#                 # Initialize Azure OpenAI client
#                 self.client = AzureOpenAI(
#                     azure_endpoint=self.endpoint,
#                     api_key=self.subscription_key,
#                     api_version="2025-01-01-preview",
#                 )
#                 self.initialized = True
#             except Exception as e:
#                 logger.error(f"Failed to initialize AzureOpenAI client: {str(e)}")
#                 raise

#     def generate_response(self, message_body: str, wa_id: str, name: str) -> str:
#         """
#         Generate a response using Azure OpenAI chat completion.
        
#         Args:
#             message_body (str): The message content from the user
#             wa_id (str): WhatsApp ID of the user
#             name (str): Name of the user
            
#         Returns:
#             str: The AI's response or None if there was an error
#         """
#         try:
#             if not message_body or not message_body.strip():
#                 logger.warning(f"Empty message body received from {name} ({wa_id})")
#                 return "I received an empty message. Please type something and try again."
                
#             logger.info(f"Generating response for {name} ({wa_id}): {message_body[:100]}...")
            
#             # Create the chat completion with enhanced context
#             messages = [
#                 {
#                     "role": "system",
#                     "content": (
#                         f"You are a helpful and friendly assistant talking to {name} on WhatsApp. "
#                         "Keep responses concise, natural, and conversational. "
#                         "Use emojis occasionally to make the conversation more engaging. "
#                         "If you don't know something, be honest about it."
#                     )
#                 },
#                 {"role": "user", "content": message_body}
#             ]
            
#             response = self.client.chat.completions.create(
#                 model=self.deployment,
#                 messages=messages,
#                 # temperature=0.7,
#                 # max_tokens=300,
#                 max_completion_tokens=100000
#                 # top_p=0.9,
#                 # frequency_penalty=0.5,
#                 # presence_penalty=0.5
#             )
            
#             # Extract the response content
#             if response and response.choices and response.choices[0].message:
#                 ai_response = response.choices[0].message.content.strip()
#                 if not ai_response:
#                     logger.warning(f"Received empty response from Azure OpenAI for user {name} ({wa_id})")
#                     return "I'm not sure how to respond to that. Could you please rephrase or ask something else?"
#                 return ai_response
                
#             logger.warning(f"Unexpected response format from Azure OpenAI for user {name} ({wa_id}")
#             return "I received an unexpected response. Could you please try again?"
            
#         except Exception as e:
#             logger.error(f"Error in generate_response for {name} ({wa_id}): {str(e)}", exc_info=True)
#             return None
