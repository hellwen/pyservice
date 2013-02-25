#!/usr/bin/env python
#coding=utf-8

from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.uploads import UploadSet, IMAGES
from flask.ext.restless import APIManager
from flask.ext.login import LoginManager

__all__ = ['mail', 'db', 'cache', 'photos', 'restapi', 'login_manager']

mail = Mail()
db = SQLAlchemy()
cache = Cache()
photos = UploadSet('photos', IMAGES)
restapi = APIManager()
login_manager=LoginManager()