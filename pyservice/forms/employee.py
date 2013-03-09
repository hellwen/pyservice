#!/usr/bin/env python
#coding=utf-8

"""
    forms: employee.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, TextAreaField, HiddenField, BooleanField, SubmitField, \
        IntegerField, SelectField, DateField, TextField, ValidationError, \
        required, optional, email, equal_to, regexp

from flask.ext.babel import gettext, lazy_gettext as _ 

from pyservice.extensions import db
from pyservice.models import Employee

class DepartmentForm(Form):
    dept_name = TextField(_("Dept Name"), validators=[
                      required(message=\
                        _("You must provide an department name"))])
    description = TextAreaField(_("Description"))


class JobForm(Form):
    job_name = TextField(_("Job Name"), validators=[
                      required(message=_("You must provide an job name"))])
    description = TextAreaField(_("Description"))

GENDER_LIST = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

class EmployeeForm(Form):

    emp_code = TextField(_("Employee Code"), validators=[
                      required(message=_("You must provide an employee code"))])
    emp_name = TextField(_("Employee Name"), validators=[
                      required(message=_("You must provide an employee name"))])
    work_email = TextField(_("Work Email"))
    work_phone = TextField(_("Work Phone"))
    work_mobile = TextField(_("Work Mobile"))
    office_location = TextField(_("Office Location"))  

    # postion
    # department = SelectField(_("Department"), default=0, coerce=int, validators=[
    #                       required(message=_("You must choices a department"))])
    # job = SelectField(_("Job"), default=0, coerce=int, validators=[
    #                       required(message=_("You must choices a job"))])
    ## personal info
    gender_id = SelectField(_("Gender"), choices=GENDER_LIST, validators=[
                          required(message=_("You must choices a Gender"))])
    # marital_id = SelectField(_("Marital Status"), coerce=int, validators=[
    #                       required(message=_("You must choices a Marital Status"))])
    id_card = TextField(_("ID Card"))
    home_addr = TextField(_("Home Address"))
    date_of_birth = DateField(_("Date of Birth"), validators=[optional()], description=_("2013-01-01"))
    place_of_birth = TextField(_("Place of Birth"))

    remark = TextAreaField(_("Reamrk"))
