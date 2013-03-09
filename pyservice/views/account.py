#! /usr/bin/env python
#coding=utf-8
"""
    account.py
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

from flaskext.babel import gettext as _
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from flask.ext.login import (LoginManager, current_user, login_required,                                                                                                                                
                             login_user, logout_user, UserMixin,
                             confirm_login, fresh_login_required)

from pyservice.helpers import render_template, cached
from pyservice.extensions import db
from pyservice.permissions import admin_permission

from pyservice.models import User
from pyservice.forms import LoginForm, SignupForm

account = Module(__name__)

@account.route("/main/", methods=("GET","POST"))
def main():
    return render_template("account/main.html")    

@account.route("/login/", methods=("GET","POST"))
def login():
    form = LoginForm(login=request.args.get('login',None),
                     next=request.args.get('next',None))

    if form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.login.data,
                                                      form.password.data)

        if user and authenticated and login_user(user, remember=form.remember.data):
            # session.permanent = form.remember.data
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            flash(_("Welcome back, %(name)s", name=user.username), "success")

            return redirect(request.args.get("next") or url_for("frontend.index"))
        else:
            flash(_("Sorry, invalid login"), "error")

    return render_template("account/login.html", form=form)

@account.route("/logout/")
def logout():
    logout_user()
    flash(_("You are now logged out"), "success")
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())    

    next_url = request.args.get('next','')

    if not next_url or next_url == request.path:
        next_url = url_for("frontend.index")

    return redirect(next_url)

@account.route("/user/", methods=("GET","POST"))
@admin_permission.require()
def user():
    data = User.query.all()
    list_columns = (("username", _("User Name")), ("nickname", _("Nick Name")))
    return render_template("list.html", module="account", model="user", list_columns=list_columns, data=data)

@account.route("/user/create/", methods=("GET","POST"))
@admin_permission.require()
def user_create():
    user = User()
    form = JobForm(next=request.args.get('next',None), obj=user)

    form.employee_id.choices = [(0, "--------------")]
    form.employee_id.choices.extend([(g.id, g.emp_name) for g in Employee.query.filter_by(active=True).order_by('emp_name')])

    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('hr.main')

        return redirect(url_for('hr.job'))

    return render_template("hr/job.html", form=form)

@account.route("/user/edit=<int:id>/", methods=("GET","POST"))
@admin_permission.require()
def user_edit(id):
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

@account.route("/user/delete=<int:id>/", methods=("GET","POST"))
@admin_permission.require()
def user_delete(id):
    job = Job.query.get(id)
    if job:
        job.delete()
    return redirect(url_for("hr.job"))    

@account.route("/permission/", methods=("GET","POST"))
@admin_permission.require()
def permission():
    job = Job()
    list_columns = dict(job_name=_("Job"), last_name='Last Name')
    data = job.joinall()
    pkfield = ''
    return render_template("list.html", folder="hr", link="hr.job", showfields=showfields, data=job.joinall())    