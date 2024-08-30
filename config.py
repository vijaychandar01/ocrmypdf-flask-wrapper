import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    PROCESSED_FOLDER = os.getenv('PROCESSED_FOLDER', 'processed')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
