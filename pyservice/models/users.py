#!/usr/bin/env python
#coding=utf-8
"""
    models: users.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import hashlib

from datetime import datetime

from flask import abort, current_app

from flask.ext.sqlalchemy import BaseQuery
from flask.ext.login import UserMixin

from pyservice.extensions import db, cache
from .employees import Employee

class UserQuery(BaseQuery):

    def authenticate(self, login, password):
        
        user = self.filter(User.username==login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

class User(db.Model, UserMixin):

    query_class = UserQuery
    
    MEMBER = 100
    ADMIN = 200

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    _password = db.Column("password", db.String(80), nullable=False)
    role = db.Column(db.Integer, default=MEMBER)
    employee_id = db.Column(db.Integer, db.ForeignKey(Employee.id))
    employee = db.relationship(Employee, foreign_keys=employee_id, backref='emp')
    active = db.Column(db.Boolean, default=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    # def __init__(self, username, nickname, email, role):
    #     self.username = username
    #     self.nickname = nickname
    #     self.email = email
    #     self.role = role

    def __str__(self):
        return self.username
    
    def _get_password(self):
        return self._password
    
    def _set_password(self, password):
        self._password = hashlib.md5(password).hexdigest()
    
    password = db.synonym("_password", 
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self,password):
        if self.password is None:
            return False        
        return self.password == hashlib.md5(password).hexdigest()
   