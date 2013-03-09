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
from flask.ext.login import (LoginManager, current_user, login_required,                                                                                                                                
                             login_user, logout_user, UserMixin,
                             confirm_login, fresh_login_required)

from pyservice.helpers import render_template, cached
from pyservice.extensions import db

from pyservice.models import User, Employee
from pyservice.forms import LoginForm, UserForm

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

            flash(_("Welcome back, %(name)s", name=user.username), "success")

            return redirect(request.args.get("next") or url_for("frontend.index"))
        else:
            flash(_("Sorry, invalid login"), "error")

    return render_template("account/login.html", form=form)

@account.route("/logout/")
def logout():
    logout_user()
    flash(_("You are now logged out"), "success")

    next_url = request.args.get('next','')

    if not next_url or next_url == request.path:
        next_url = url_for("frontend.index")

    return redirect(next_url)

@account.route("/user/", methods=("GET","POST"))
def user():
    data = User.query.all()
    list_columns = (("username", _("User Name")), ("nickname", _("Nick Name")))
    return render_template("list.html", module="account", model="user", list_columns=list_columns, data=data)

@account.route("/user/create/", methods=("GET","POST"))
def user_create():
    form = UserForm(next=request.args.get('next',None))

    form.employee_id.choices = [(0, "")]
    form.employee_id.choices.extend([(g.id, g.dept_name) for g in Employee.query.filter_by(active=True).order_by('emp_name')])

    if form.validate_on_submit():

        user = User(role=100)
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash(_("Welcome, %(name)s", name=user.username), "success")

        next_url = form.next.data

        if not next_url or next_url == request.path:
            next_url = url_for('account.main', username=user.username)

        return redirect(next_url)

    return render_template("account/user.html", form=form)

@account.route("/user/edit=<int:id>/", methods=("GET","POST"))
def user_edit(id):
    user = User.query.get(id)
    form = UserForm(next=request.args.get('next',None), obj=user)

    form.employee_id.choices = [(0, "")]
    form.employee_id.choices.extend([(g.id, g.dept_name) for g in Employee.query.filter_by(active=True).order_by('emp_name')])

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('account.main')

        return redirect(url_for('account.user'))

    return render_template("account/user.html", form=form)

@account.route("/user/delete=<int:id>/", methods=("GET","POST"))
def user_delete(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("account.user"))    

@account.route("/permission/", methods=("GET","POST"))
def permission():
    job = Job()
    list_columns = dict(job_name=_("Job"), last_name='Last Name')
    data = job.joinall()
    pkfield = ''
    return render_template("list.html", folder="hr", link="hr.job", showfields=showfields, data=job.joinall())    