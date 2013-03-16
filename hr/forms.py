#!/usr/bin/env python
#coding=utf-8

"""
    forms: employee.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, HiddenField, TextAreaField, SelectField,\
    DateField, TextField, required, optional

from flask.ext.babel import lazy_gettext as _


class DepartmentForm(Form):
    next = HiddenField()

    dept_name = TextField(_("Dept Name"), validators=[
        required(message=_("You must provide an department name"))])
    description = TextAreaField(_("Description"))


class JobForm(Form):
    next = HiddenField()

    job_name = TextField(_("Job Name"), validators=[
        required(message=_("You must provide an job name"))])
    description = TextAreaField(_("Description"))


class EmployeeForm(Form):
    next = HiddenField()

    emp_code = TextField(_("Employee Code"), validators=[
        required(message=_("You must provide an employee code"))])
    emp_name = TextField(_("Employee Name"), validators=[
        required(message=_("You must provide an employee name"))])
    work_email = TextField(_("Work Email"))
    work_phone = TextField(_("Work Phone"))
    work_mobile = TextField(_("Work Mobile"))
    office_location = TextField(_("Office Location"))

    # # postion
    department_id = SelectField(_("Department"), default=0, coerce=int,
        validators=[
            required(message=_("You must choices a department"))])
    job_id = SelectField(_("Job"), default=0, coerce=int,
        validators=[
            required(message=_("You must choices a job"))])
    # ## personal info
    gender_id = SelectField(_("Gender"), coerce=int, validators=[
        required(message=_("You must choices a Gender"))])
    id_card = TextField(_("ID Card"))
    home_addr = TextField(_("Home Address"))
    date_of_birth = DateField(_("Date of Birth"), validators=[optional()],
        description=_("2013-01-01"))

    remark = TextAreaField(_("Reamrk"))
