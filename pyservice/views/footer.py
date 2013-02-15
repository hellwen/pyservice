
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


from pyservice.helpers import render_template, cached
from pyservice.permissions import auth, admin 
from pyservice.extensions import db

from pyservice.models import User, UserCode
from pyservice.forms import LoginForm, SignupForm

footer = Module(__name__)

@footer.route("/about")
def about():
    return render_template("footer/about.html")