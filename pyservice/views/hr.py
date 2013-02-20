#! /usr/bin/env python
#coding=utf-8
"""
    sales.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import datetime
import os, sys

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
from pyservice.extensions import db

from pyservice.models import Employee, Department, Job
from pyservice.forms import EmployeeForm, DepartmentForm, JobForm

hr = Module(__name__)

@hr.route("/main/", methods=("GET","POST"))
def main():
    return render_template("hr/main.html")

@hr.route("/employee/", methods=("GET","POST"))
def employee():
    employee = db.session.execute(" \
        select a.id, a.emp_code, a.emp_name, a.work_addr, a.work_email, a.work_phone, a.work_mobile, \
            a.office_location, b.emp_name as related_user, c.dept_name as department, d.job_name as job, \
            a.level, e.emp_name as manager, a.is_manager, a.date_of_leaved, a.gender, a.marital, \
            a.num_children, a.id_card, a.home_addr, a.date_of_birth, a.place_of_birth, a.remark \
        from employees a \
        left join employees b on b.id = a.related_user \
        left join departments c on c.id = a.department \
        left join jobs d on d.id = a.job \
        left join employees e on e.id = a.manager \
        ")
    showfields = (("emp_code", _("Employee Code")), ("emp_name", _("Employee")), ("work_addr", _("Work Address")), 
        ("work_email", _("Work Email")), ("work_phone", _("Work Phone")), ("work_mobile", _("Work Mobile")),
        ("office_location", _("Office Location")), ("related_user", _("Related User")), ("department", _("Department")),
        ("job", _("Job")), ("level", _("Level")), ("manager", _("Manager")), ("is_manager", _("Is Manager")), 
        ("gender", _("Gender")), ("marital", _("Marital")),  ("num_children", _("Number Children")), 
        ("id_card", _("ID Card")), ("home_addr", _("Home Address")), ("date_of_birth", _("Date of Birth")),
        ("place_of_birth", _("Place of Birth")), ("remark", _("Remark")))
    return render_template("list.html", folder="hr", link="hr.employee", showfields=showfields, table=employee)

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
    form.related_user.choices.extend([(g.id, g.emp_name) for g in Employee.query.order_by('emp_name')])
    form.department.choices = [(g.id, g.dept_name) for g in Department.query.order_by('dept_name')]
    form.job.choices = [(g.id, g.job_name) for g in Job.query.order_by('job_name')]
    form.manager.choices = [(0, "")]
    form.manager.choices.extend([(g.id, g.emp_name) for g in Employee.query.order_by('emp_name')])

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
    department = db.session.execute(" \
        select a.id, a.dept_name, c.emp_name as manager, b.dept_name as parent_department \
        from departments a \
        left join departments b on b.id = a.parent_department \
        left join employees c on c.id = a.manager \
        ")
    showfields = (("dept_name", _("Department")), ("manager", _("Manager")), ("parent_department", _("Parent Department")))
    return render_template("list.html", folder="hr", link="hr.department", showfields=showfields, table=department)


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
    form.manager.choices.extend([(g.id, g.emp_name) for g in Employee.query.order_by('emp_name')])
    form.parent_department.choices = [(0, "")]
    form.parent_department.choices.extend([(g.id, g.dept_name) for g in Department.query.order_by('dept_name')])
    
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
    job = db.session.execute(" \
        select a.id, a.job_name, b.dept_name as department, a.description \
        from jobs a \
        left join departments b on b.id = a.department \
        ")
    showfields = (("job_name", _("Job")), ("department", _("Department")), ("description", _("Description")))
    return render_template("list.html", folder="hr", link="hr.job", showfields=showfields, table=job)

@hr.route("/job/edit=<int:id>/", methods=("GET","POST"))
def job_edit(id):
    # is add
    if id==0:
        job = Job()
    # is edit
    else:
        job = Job.query.get(id)

    form = JobForm(next=request.args.get('next',None), obj=job)

    form.department.choices = [(0, "")]
    form.department.choices.extend([(g.id, g.dept_name) for g in Department.query.order_by('dept_name')])

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