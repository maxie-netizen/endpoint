import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'

    # Database (uses instance folder)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload/download settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')

    # API key expiry
    API_KEY_EXPIRY_DAYS = 30
