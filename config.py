import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mcb-smart-construction-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "database", "construction.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads
    UPLOAD_FOLDER = (
        os.path.join('/tmp', 'mcb-uploads')
        if os.environ.get('VERCEL')
        else os.path.join(BASE_DIR, 'static', 'uploads')
    )
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'pdf', 'docx'}
    
    # ML Models directory
    ML_MODEL_DIR = os.path.join(BASE_DIR, 'ml_models')
    
    # Company Profile Settings (MCB Defaults)
    COMPANY_NAME = "MAMATHA CONSTRUCTIONS & BUILDERS (MCB)"
    PRIMARY_BUILDER = "SARGU SANJU"
    OFFICE_ADDRESS = "Vishwanath Colony, Near Hanuman Temple, Shambunipet, Warangal, Telangana 506005, India"
    PHONE = "+91 7386181866"
    SERVICE_AREA = "Warangal, Hanamkonda, Kazipet and surrounding Telangana regions"
    TAGLINE_EN = "Building Your Dreams with Trust, Quality and Care."
    TAGLINE_TE = "నమ్మకం, నాణ్యత, శ్రద్ధతో మీ కలల ఇంటి నిర్మాణం."
    
    # Weather Default Location (Warangal, Telangana)
    DEFAULT_LAT = 17.9689
    DEFAULT_LON = 79.5941
    DEFAULT_CITY = "Warangal"
