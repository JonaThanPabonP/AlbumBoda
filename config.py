import secrets
from sqlalchemy import create_engine

class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = secrets.token_hex(16)
    UPLOAD_FOLDER = 'static/fotos'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    SQLALCHEMY_DATABASE_URI = 'mysql://ujiigtehwj0vwbqa:H5X4AWjuSxZrK9JOQLwW@ba2y64hw2lqplqemrpqs-mysql.services.clever-cloud.com:3306/ba2y64hw2lqplqemrpqs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    engine = create_engine(SQLALCHEMY_DATABASE_URI)