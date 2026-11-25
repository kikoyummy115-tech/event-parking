import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")
    
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # Tests the connection with a quick 'SELECT 1' before using it
        "pool_recycle": 280,    # Recycles connections older than 280 seconds (under 5 mins)
    }