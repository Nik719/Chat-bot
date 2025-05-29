import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    VERSION = os.getenv('VERSION', 'v17.0')
    PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
