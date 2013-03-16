#! /usr/bin/env python
#coding=utf-8
"""
    frontend.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, render_template

frontend = Blueprint("frontend", __name__,
    url_prefix="/",
    static_url_path='static')


@frontend.route("/", methods=("GET", "POST"))
@frontend.route("/index/", methods=("GET", "POST"))
def index():
    return render_template("index.html")


@frontend.route("/about/", methods=("GET", "POST"))
def about():
    return render_template("about.html")
