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

from flaskext.babel import gettext as _
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from flask.ext.login import (LoginManager, current_user, login_required,                                                                                                                                
                             login_user, logout_user, UserMixin,
                             confirm_login, fresh_login_required)

from pyservice.helpers import render_template, cached
from pyservice.permissions import auth, admin 
from pyservice.extensions import db

from pyservice.models import User, UserCode
from pyservice.forms import LoginForm, SignupForm

sales = Module(__name__)

@sales.route("/main", methods=("GET","POST"))
def main():
    return render_template("sales/main.html")

@sales.route("/order", methods=("GET","POST"))
def order():
    return render_template("sales/order.html")

@sales.route("/assign", methods=("GET","POST"))
def assign():
    return render_template("sales/assign.html")

@sales.route("/feedback", methods=("GET","POST"))
def feedback():
    return render_template("sales/feedback.html")