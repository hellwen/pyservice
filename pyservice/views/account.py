#! /usr/bin/env python
#coding=utf-8
"""
    account.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, request, flash, redirect, url_for, render_template

from flaskext.babel import gettext as _

from pyservice.extensions import db

from pyservice.models import User
from pyservice.forms import LoginForm, UserForm


account = Blueprint("account", __name__,
    url_prefix="/account",
    template_folder='templates',
    static_url_path='static')


@account.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("account/main.html")


@account.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.login.data,
                                                      form.password.data)

        # if user and authenticated and login_user(user,
        #     remember=form.remember.data):
        #     flash(_("Welcome back, %(name)s", name=user.username), "success")

        #     return redirect(request.args.get("next") or
        #         url_for("frontend.index"))
        # else:
        #     flash(_("Sorry, invalid login"), "error")

    return render_template("account/login.html", form=form)


@account.route("/logout/")
def logout():
    # logout_user()
    flash(_("You are now logged out"), "success")

    next_url = request.args.get('next', '')

    if not next_url or next_url == request.path:
        next_url = url_for("frontend.index")

    return redirect(next_url)


@account.route("/user/", methods=("GET", "POST"))
def user():
    data = User.query.all()
    list_columns = (("username", _("User Name")),)
    return render_template("list.html", module="account", model="user",
        list_columns=list_columns, data=data)


@account.route("/user/create/", methods=("GET", "POST"))
def user_create():
    form = UserForm(next=request.args.get('next', None))

    # form.employee.choices = [(1, "1"),]
    # form.employee.choices.extend([(g.id, g.dept_name) for g in
        # Employee.query.filter_by(active=True).order_by('emp_name')])

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash(_("Welcome, %(name)s", name=user.username), "success")

        next_url = form.next.data

        if not next_url or next_url == request.path:
            next_url = url_for('account.main', username=user.username)

        return redirect(next_url)

    return render_template("account/user.html", form=form)


@account.route("/user/edit=<int:id>/", methods=("GET", "POST"))
def user_edit(id):
    user = User.query.get(id)
    form = UserForm(next=request.args.get('next', None), obj=user)

    form.employee_id.choices = [(0, "")]
    form.employee_id.choices.extend([(g.id, g.dept_name) for g in
        Employee.query.filter_by(active=True).order_by('emp_name')])

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('account.main')

        return redirect(url_for('account.user'))

    return render_template("account/user.html", form=form)


@account.route("/user/delete=<int:id>/", methods=("GET", "POST"))
def user_delete(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("account.user"))
