#!/usr/bin/env python
#coding=utf-8

"""
    forms: account.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, TextAreaField, HiddenField, BooleanField, \
        PasswordField, SubmitField, TextField, ValidationError, SelectField, \
        required, optional, equal_to, regexp

from flask.ext.babel import gettext, lazy_gettext as _ 

from pyservice.extensions import db
from pyservice.models import User

class LoginForm(Form):
    login = TextField(_("Username"), validators=[
                      required(message=_("You must provide an email or username"))])
    password = PasswordField(_("Password"), validators=[
                      required(message=_("You must provide an password"))])
    remember = BooleanField(_("Remember me"))
    next = HiddenField()
    submit = SubmitField(_("Login"))

class UserForm(Form):

    username = TextField(_("Username"), validators=[
                         required(message=_("Username required"))])

    password = TextField(_("Password"), validators=[
                             required(message=_("Password required"))])

    employee = SelectField(_("Relation Employee"), validators=[optional()], choices=[(1, 'a'), 2, 'b'])

    next = HiddenField()

    submit = SubmitField(_("Save"))