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

from .validators import is_username

class EmployeeForm(Form):

    emp_code = TextField(_("Employee Code"), validators=[
                      required(message=_("You must provide an employee code"))])
    emp_name = TextField(_("Name"), validators=[
                      required(message=_("You must provide an employee name"))])
    work_addr = TextField(_("Working Address"))
    work_email = TextField(_("Work Email"))
    work_phone = TextField(_("Work Phone"))
    work_mobile = TextField(_("Work Mobile"))
    office_location = TextField(_("Office Location"))  
    related_user = SelectField(_("Related User"), default=0, coerce=int, validators=[optional()])

    remark = TextAreaField(_("Reamrk"))
    
    # postion
    department = SelectField(_("Department"), default=0, coerce=int, validators=[
                          required(message=_("You must choices a department"))])
    job = SelectField(_("Job"), default=0, coerce=int, validators=[
                          required(message=_("You must choices a job"))])
    level = SelectField(_("Level"), default=0, coerce=int, validators=[optional()],
        choices=[(0, ""),(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5"),(6,"6"),(7,"7"),(8,"8"),(9,"9")])
    manager = SelectField(_("Mnager"), default=0, coerce=int, validators=[optional()])
    is_manager = BooleanField(_('Is a Mnager'))

    ## personal info
    # status
    gender = SelectField(_("Gender"), coerce=int, choices=[
                                      (Employee.MALE, "Male"),
                                      (Employee.FEMALE, "Female")])
    marital = SelectField(_("Marital Status"), coerce=int, choices=[
                                      (Employee.SINGLE, "Single"), 
                                      (Employee.MARRIED, "Married"), 
                                      (Employee.DIVORCED, "Divorced")])
    num_children = IntegerField(_("Number of Children"), default=0)
    # contact
    id_card = TextField(_("ID Card"))
    home_addr = TextField(_("Home Address"))
    # birth
    date_of_birth = DateField(_("Date of Birth"), validators=[optional()], description=_("2013-01-01"))
    place_of_birth = TextField(_("Place of Birth"))

    next = HiddenField()

    submit = SubmitField(_("Save"))


class DepartmentForm(Form):

    dept_name = TextField(_("Name"), validators=[
                      required(message=\
                        _("You must provide an department name"))])
    manager = SelectField(_("Manager"), default=0, coerce=int, validators=[optional()])
    parent_department = SelectField(_("Parent Department"), default=0, coerce=int, validators=[optional()])

    next = HiddenField()

    submit = SubmitField(_("Save"))


class JobForm(Form):

    job_name = TextField(_("Name"), validators=[
                      required(message=_("You must provide an job name"))])
    department = SelectField(_("Department"), default=0, coerce=int, validators=[optional()])
    description = TextAreaField(_("Description"))

    next = HiddenField()    

    submit = SubmitField(_("Save"))

