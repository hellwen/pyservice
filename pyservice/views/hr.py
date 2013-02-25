#! /usr/bin/env python
#coding=utf-8
"""
    sales.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import datetime
import os, sys
import urllib2

# parse_qsl moved to urlparse module in v2.6
try:
    from urlparse import parse_qsl
except:
    from cgi import parse_qsl

from flask import Module, Response, request, flash, jsonify, g, current_app,\
    abort, redirect, url_for, session

from flask.ext.babel import gettext as _
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from flask.ext.login import (LoginManager, current_user, login_required,                                                                                                                                
                             login_user, logout_user, UserMixin,
                             confirm_login, fresh_login_required)

from pyservice.helpers import render_template, cached
from pyservice.permissions import auth, admin 
from pyservice.extensions import db, restapi

from pyservice.models import Employee, Department, Job, Item
from pyservice.forms import EmployeeForm, DepartmentForm, JobForm, ItemForm

hr = Module(__name__)

@hr.route("/main/", methods=("GET","POST"))
def main():
    return render_template("hr/main.html")

@hr.route("/employee/", methods=("GET","POST"))
def employee():
    employee = Employee()
    showfields = (("emp_code", _("Employee Code")), ("emp_name", _("Employee")), 
        ("job", _("Job")), ("department", _("Department")), ("level", _("Level")), ("manager", _("Manager")), ("is_manager", _("Is Manager")), 
        ("gender", _("Gender")), ("id_card", _("ID Card")))
    return render_template("list.html", folder="hr", link="hr.employee", showfields=showfields, table=employee.joinall())

@hr.route("/employee/edit=<int:id>/", methods=("GET","POST"))
def employee_edit(id):
    # is add
    if id==0:
        employee = Employee()
    # is edit
    else:
        employee = Employee().query.get(id)

    form = EmployeeForm(next=request.args.get('next',None), obj=employee)

    form.related_user.choices = [(0, "")]
    form.related_user.choices.extend([(g.id, g.emp_name) for g in Employee.query.filter_by(active=True).order_by('emp_name')])
    form.department.choices = [(g.id, g.dept_name) for g in Department.query.filter_by(active=True).order_by('dept_name')]
    form.job.choices = [(g.id, g.job_name) for g in Job.query.filter_by(active=True).order_by('job_name')]
    form.gender_id.choices = [(g.item_id, g.item_name) for g in Item.query.filter_by(active=True, group_id=10).order_by('item_id')]
    form.marital_id.choices = [(g.item_id, g.item_name) for g in Item.query.filter_by(active=True, group_id=20).order_by('item_id')]
    form.manager.choices = [(0, "")]
    form.manager.choices.extend([(g.id, g.emp_name) for g in Employee.query.filter_by(active=True).order_by('emp_name')])

    if form.validate_on_submit():
        form.populate_obj(employee)
        employee.save()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('hr.main')

        return redirect(url_for('hr.employee'))

    return render_template("hr/employee.html", form=form)   


@hr.route("/job/delete=<int:id>/", methods=("GET","POST"))
def employee_delete(id):
    employee = Employee.query.get(id)
    if employee:
        employee.delete()
    return redirect(url_for("hr.employee"))    


@hr.route("/department/", methods=("GET","POST"))
def department():
    department = Department()
    showfields = (("dept_name", _("Department")), ("manager", _("Manager")), ("parent_department", _("Parent Department")))
    return render_template("list.html", folder="hr", link="hr.department", showfields=showfields, table=department.joinall())

@hr.route("/department/edit=<int:id>/", methods=("GET","POST"))
def department_edit(id):
    # is add
    if id==0:
        department = Department()
    # is edit
    else:
        department = Department.query.get(id)

    form = DepartmentForm(next=request.args.get('next',None), obj=department)

    form.manager.choices = [(0, "")]
    form.manager.choices.extend([(g.id, g.emp_name) for g in Employee.query.filter_by(active=True).order_by('emp_name')])
    form.parent_id.choices = [(0, "")]
    form.parent_id.choices.extend([(g.id, g.dept_name) for g in Department.query.filter_by(active=True).order_by('dept_name')])
    
    if form.validate_on_submit():
        form.populate_obj(department)
        department.save()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for("hr.main")

        return redirect(url_for("hr.department"))

    return render_template("hr/department.html", form=form)

@hr.route("/department/delete=<int:id>/", methods=("GET","POST"))
def department_delete(id):
    department = Department.query.get(id)
    if department:
        department.delete()
    return redirect(url_for("hr.department"))

@hr.route("/job/", methods=("GET","POST"))
def job():
    job = Job()
    showfields = (("job_name", _("Job")), ("department", _("Department")), ("description", _("Description")))
    return render_template("list.html", folder="hr", link="hr.job", showfields=showfields, table=job.joinall())

@hr.route("/job/edit=<int:id>/", methods=("GET","POST"))
def job_edit(id):
    # is add
    if id==0:
        job = Job()
    # is edit
    else:
        job = Job.query.get(id)

    form = JobForm(next=request.args.get('next',None), obj=job)

    form.department_id.choices = [(0, "")]
    form.department_id.choices.extend([(g.id, g.dept_name) for g in Department.query.filter_by(active=True).order_by('dept_name')])

    if form.validate_on_submit():
        form.populate_obj(job)
        job.save()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('hr.main')

        return redirect(url_for('hr.job'))

    return render_template("hr/job.html", form=form)

@hr.route("/job/delete=<int:id>/", methods=("GET","POST"))
def job_delete(id):
    job = Job.query.get(id)
    if job:
        job.delete()
    return redirect(url_for("hr.job"))

@hr.route("/item/", methods=("GET","POST"))
def item():
    item = Item()
    showfields = (("group_id", _("Group Id")), ("group_name", _("Group Name")), ("item_id", _("Item Id")), ("item_name", _("Item Name")))
    return render_template("list.html", folder="hr", link="hr.item", showfields=showfields, table=item.joinall())

@hr.route("/item/edit=<int:id>/", methods=("GET","POST"))
def item_edit(id):
    # is add
    if id==0:
        item = Item()
    # is edit
    else:
        item = Item.query.get(id)

    form = ItemForm(next=request.args.get('next',None), obj=item)

    if form.validate_on_submit():
        form.populate_obj(item)
        item.save()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('hr.main')

        return redirect(url_for('hr.item'))

    return render_template("hr/item.html", form=form)

@hr.route("/item/delete=<int:id>/", methods=("GET","POST"))
def item_delete(id):
    item = Item.query.get(id)
    if item:
        item.delete()
    return redirect(url_for("hr.item"))