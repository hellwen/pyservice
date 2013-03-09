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
from flask.ext.admin.contrib import sqlamodel
from flask.ext.admin import expose

from pyservice.helpers import render_template, cached
from pyservice.extensions import db, admin
from pyservice.permissions import admin_permission

from pyservice.models import User
from pyservice.forms import LoginForm, SignupForm

account = Module(__name__)

class LoginAdmin(sqlamodel.ModelView):
    form = LoginForm

    list_template = 'account/login.html'

    column_list = ('login', 'password', 'remember')

    # Views
    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        if g.user:
            logout_user()
            flash(_("You are now logged out"), "success")
            identity_changed.send(current_app._get_current_object(),
                                  identity=AnonymousIdentity())    

            # next_url = request.args.get('next','')

            # if not next_url or next_url == request.path:
                # next_url = url_for("frontend.index")

            return redirect(url_for("frontend.index"))
        else:
            form1 = LoginForm(login=request.args.get('login',None),
                            next=request.args.get('next',None))
            if form1.validate_on_submit():
                user, authenticated = User.query.authenticate(form1.login.data,
                                                              form1.password.data)

                if user and authenticated and login_user(user, remember=form1.remember.data):
                    identity_changed.send(current_app._get_current_object(),
                                          identity=Identity(user.id))

                    flash(_("Welcome back, %(name)s", name=user.username), "success")

                    # return redirect(request.args.get("next") or url_for("frontend.index"))
                    return redirect(url_for("frontend.index"))
                else:
                    flash(_("Sorry, invalid login"), "error")

            return self.render(self.list_template, form=form1)

    def __init__(self, session, **kwargs):
        super(LoginAdmin, self).__init__(User, session, **kwargs)

admin.add_view(LoginAdmin(db.session, name=_("Login"), endpoint="login"))


@account.route("/main/", methods=("GET","POST"))
def main():
    return render_template("account/main.html")    


@account.route("/login/", methods=("GET", "POST"))
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

    return render_template("admin/login", form=form)

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
