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

# from flask.ext.sqlalchemy import BaseQuery
import flask.ext.sqlalchemy
# import sqlalchemy
from flask.ext.principal import RoleNeed, UserNeed, Permission
from flask.ext.login import UserMixin
import flask.ext.restless

from pyservice.extensions import db, cache, restapi
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
    gender_id = db.Column(db.Integer, nullable=False)
    marital_id = db.Column(db.Integer, nullable=False)
    num_children = db.Column(db.Integer, default=0, nullable=False)
    # contact
    id_card = db.Column(db.String(50))
    home_addr = db.Column(db.String(100))
    # birth
    date_of_birth = db.Column(db.DateTime)
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

    def joinall(self):
        return db.session.execute(" \
            select a.id, a.emp_code, a.emp_name, a.work_addr, a.work_email, a.work_phone, a.work_mobile, \
                a.office_location, b.emp_name as related_user, c.dept_name as department, d.job_name as job, \
                a.level, e.emp_name as manager, a.is_manager, a.date_of_leaved, f.item_name as gender, i.item_name as marital, \
                a.num_children, a.id_card, a.home_addr, a.date_of_birth, a.place_of_birth, a.remark \
            from employees a \
            left join employees b on b.id = a.related_user \
            left join departments c on c.id = a.department \
            left join jobs d on d.id = a.job \
            left join employees e on e.id = a.manager \
            left join items f on f.item_id = a.gender_id \
            left join items i on i.item_id = a.gender_id \
            ")        

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
    parent_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    parent = db.relationship("Department", foreign_keys=parent_id, remote_side=id)
    active = db.Column(db.Boolean, default=True)

    def joinall(self):
        return db.session.execute(" \
        select a.id, a.dept_name, c.emp_name as manager, b.dept_name as parent_department \
        from departments a \
        left join departments b on b.id = a.parent_id \
        left join employees c on c.id = a.manager \
        where a.active = 1 \
        ")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

class Job(db.Model):

    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(50), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    # department = db.relationship("Department", foreign_keys=department_id, remote_side=id)

    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)

    def joinall(self):
        return db.session.execute(" \
            select a.id, a.job_name, a.department_id, b.dept_name as department, a.description \
            from jobs a \
            left join departments b on b.id = a.department_id \
            where a.active = 1 \
            ")
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False, index=True)
    group_name = db.Column(db.String(30), nullable=False)
    item_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    item_order = db.Column(db.Integer, default=0)
    item_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, *args):
        if len(args) == 5:
            self.group_id = args[0]
            self.group_name = args[1]
            self.item_id = args[2]
            self.item_order = args[3]
            self.item_name = args[4]
            self.active = True
        else:        
            super(Item, self).__init__(*args)

    # def __init__(self, group_id, group_name, item_id, item_name):
        # self.group_id = group_id
        # self.group_name = group_name
        # self.item_id = item_id
        # self.item_name = item_name
        # self.active = True       

    def joinall(self):
        return db.session.execute(" \
            select id, group_id, group_name, item_id, item_order, item_name \
            from items \
            where active = 1 \
            order by group_id, item_order \
            ")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

