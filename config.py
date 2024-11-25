import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')

class OAuth:
    GOOGLE_CLIENT_ID = "463383199138-ua2bpp0et6eiap77vnd82t9hj12qqmim.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"
