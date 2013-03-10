#! /usr/bin/env python
#coding=utf-8
"""
    frontend.py
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

from flask import Module
from flaskext.babel import gettext as _

from pyservice.helpers import render_template
from pyservice.extensions import db

frontend = Module(__name__)

@frontend.route("/", methods=("GET","POST"))
@frontend.route("/index", methods=("GET","POST"))
def index():
    return render_template("index.html")

@frontend.route("/about", methods=("GET","POST"))
def about():
    return render_template("about.html")