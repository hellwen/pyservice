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

from .validators import is_username

class LoginForm(Form):
    login = TextField(_("Username"), validators=[
                      required(message=_("You must provide an email or username"))])
    password = PasswordField(_("Password"), validators=[
                      required(message=_("You must provide an password"))])
    remember = BooleanField(_("Remember me"))
    next = HiddenField()
    submit = SubmitField(_("Login"))

ROLE_LIST = (
    (100, _('Member')),
    (200, _('Admin')),
)

class UserForm(Form):

    username = TextField(_("Username"), validators=[
                         required(message=_("Username required"))])

    password = PasswordField(_("Password"), validators=[
                             required(message=_("Password required"))])

    # password_again = PasswordField(_("Password again"), validators=[
    #                                equal_to("password", message=\
    #                                         _("Passwords don't match"))])

    role = SelectField(_("Role"), choices=ROLE_LIST, validators=[optional])

    employee_id = SelectField(_("Relation Employee"), validators=[optional])

    next = HiddenField()

    submit = SubmitField(_("Signup"))