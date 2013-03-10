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

from pyservice.extensions import db
from .employees import Employee

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(Employee.id), nullable=True)
    employee = db.relationship(Employee, foreign_keys=employee_id, backref='emp')
    active = db.Column(db.Boolean, default=True)
