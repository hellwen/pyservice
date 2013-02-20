#!/usr/bin/env python
#coding=utf-8
"""
    models: employee.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime

from werkzeug import cached_property

from flask import abort, current_app

from flask.ext.sqlalchemy import BaseQuery
from flask.ext.principal import RoleNeed, UserNeed, Permission
from flask.ext.login import UserMixin

from pyservice.extensions import db, cache
from pyservice.permissions import admin


# class EmployeeQuery(BaseQuery):
    
#     def search(self, key):
#         query = self.filter(db.or_(Employee.emp_code.ilike('%'+key+'%'),
#                                    Employee.emp_name.ilike('%'+key+'%')))
#         return query

#     def get_by_emp_code(self, emp_code):
#         employee = self.filter(Employee.emp_code==emp_code).first()
#         if employee is None:
#             abort(404)
#         return employee

#     def get_by_emp_name(self, emp_name):
#         employee = self.filter(Employee.emp_name==emp_name).first()
#         if employee is None:
#             abort(404)
#         return employee


class Employee(db.Model, UserMixin):

    __tablename__ = 'employees'
    
    # query_class = EmployeeQuery
    
    id = db.Column(db.Integer, primary_key=True)
    emp_code = db.Column(db.String(20), unique=True)
    emp_name = db.Column(db.String(50), unique=True)

    ## public info
    # contact
    work_addr = db.Column(db.String(100))
    work_email = db.Column(db.String(100))
    work_phone = db.Column(db.String(50))
    work_mobile = db.Column(db.String(50))
    office_location = db.Column(db.String(100))
    related_user = db.Column(db.Integer, default=0)
    remark = db.Column(db.String(300))
    # postion
    department = db.Column(db.Integer, default=0, nullable=False)
    job = db.Column(db.Integer, default=0, nullable=False)
    level = db.Column(db.Integer, default=0)
    manager = db.Column(db.Integer, default=0)
    is_manager = db.Column(db.Integer, default=0)
    # leaves 
    date_of_leaved = db.Column(db.DateTime)
    ## personal info
    # status
    MALE=100
    FEMALE=200
    gender = db.Column(db.Integer, default=MALE, nullable=False)
    SINGLE=100
    MARRIED=200
    DIVORCED=300
    marital = db.Column(db.Integer, default=SINGLE, nullable=False)
    num_children = db.Column(db.Integer, default=0, nullable=False)
    # contact
    id_card = db.Column(db.String(50))
    home_addr = db.Column(db.String(100))
    # birth
    date_of_birth = db.Column(db.DateTime, default=datetime.utcnow)
    place_of_birth = db.Column(db.String(100))
    ## manage info
    active = db.Column(db.Boolean, default=True)


    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj
    
        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.id)) & admin
  
    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.emp_name
    
    def __repr__(self):
        return "<%s>" % self
    
    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Department(db.Model, UserMixin):

    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(50), unique=True)
    manager = db.Column(db.Integer, default=0)
    parent_department = db.Column(db.Integer, default=0)
    ## manage info
    active = db.Column(db.Boolean, default=True)

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj
    
        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.id)) & admin
  
    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.dept_name
    
    def __repr__(self):
        return "<%s>" % self
    
    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

class Job(db.Model, UserMixin):

    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(50), unique=True)
    department = db.Column(db.Integer, default=0)
    description = db.Column(db.String(500))
    ## manage info
    active = db.Column(db.Boolean, default=True)

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj
    
        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.id)) & admin

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.job_name
    
    def __repr__(self):
        return "<%s>" % self
    
    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()        