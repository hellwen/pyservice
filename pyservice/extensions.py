from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_admin import Admin

__all__ = ['db', 'login_manager']

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin()
