#!/usr/bin/env python
#coding=utf-8

"""
    forms: base.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, TextAreaField, HiddenField, BooleanField, SubmitField, \
        IntegerField, SelectField, DateField, TextField, ValidationError, \
        required, optional, email, equal_to, regexp

from flask.ext.babel import gettext, lazy_gettext as _ 

from pyservice.extensions import db
from pyservice.models import Employee

class ItemForm(Form):

    item_id = TextField(_("Item ID"), validators=[
                      required(message=_("You must provide"))])
    item_order = TextField(_("Item Order"), validators=[
                      required(message=_("You must provide"))])    
    item_name = TextField(_("Item Name"), validators=[
                      required(message=_("You must provide"))])
    group_id = TextField(_("Group ID"), validators=[
                      required(message=_("You must provide"))])
    group_name = TextField(_("Group Name"), validators=[
                      required(message=_("You must provide"))])

    next = HiddenField()

    submit = SubmitField(_("Save"))