import secrets
from sqlalchemy import create_engine
import pyrebase

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


class Firebase:
    def __init__(self):
        self.firebase_config = {
            "apiKey": "AIzaSyCAdcR6J4RgiIYQILRfl7RUdMJCzaMb6fc",
            "authDomain": "albumboda-5f8d0.firebaseapp.com",
            "projectId": "albumboda-5f8d0",
            "storageBucket": "albumboda-5f8d0.appspot.com",
            "messagingSenderId": "1019849214546",
            "appId": "1:1019849214546:web:aff63cd59910f3ec97ed8b",
            "measurementId": "G-HTGPFZ982R"
        }
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.storage = self.firebase.storage()

    def upload_file(self, local_file_path, remote_file_path):
        self.storage.child(remote_file_path).put(local_file_path)

    def download_file(self, remote_file_path, local_file_path):
        self.storage.child(remote_file_path).download(local_file_path)