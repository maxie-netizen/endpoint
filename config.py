import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///../database/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    DOWNLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'downloads')
    API_KEY_EXPIRY_DAYS = 30  # Default API key expiry period
