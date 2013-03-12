#!/usr/bin/env python
#coding=utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.restless import APIManager
from flask.ext.login import LoginManager

__all__ = ['db', 'cache', 'restapi', 'login_manager']

db = SQLAlchemy()
cache = Cache()
restapi = APIManager()
login_manager = LoginManager()
