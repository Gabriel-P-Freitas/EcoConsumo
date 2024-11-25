from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_jwt_extended import JWTManager

from authlib.integrations.flask_client import OAuth
oauth = OAuth()

