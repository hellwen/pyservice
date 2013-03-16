#! /usr/bin/env python
#coding=utf-8
"""
    sales.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import logging

from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask.ext.babel import gettext as _

from .models import Employee, Department, Job
from .forms import EmployeeForm, DepartmentForm, JobForm

from pyservice.extensions import db

hr = Blueprint('hr', __name__,
    url_prefix="/hr",
    template_folder='templates',
    static_folder='static')


class FormBase(object):
    fieldsets = []
    field_labels = dict()
    readonly = True
    set_focus = True

    def __init__(self, db, model, form, modelname, return_url=""):
        self.db = db
        self.model = model
        self.form = form
        self.modelname = modelname
        self.return_url = return_url

    def get_field_categorys(self):
        return [(tab[0]) for tab in self.fieldsets if tab[0]]

    def is_tuple(self, field):
        return isinstance(field, tuple)

    def get_fields(self, category_name):
        for tab in self.fieldsets:
            if tab[0] == category_name and tab[1]['fields']:
                return tab[1]['fields']

    def create_model(self):
        try:
            self.form.populate_obj(self.model)
            self.db.session.add(self.model)
            self.db.session.commit()
            return True
        except Exception, ex:
            flash(_('Failed to create model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to create model')
            self.db.session.rollback()
            return False

    def update_model(self):
        try:
            self.form.populate_obj(self.model)
            self.db.session.commit()
            return True
        except Exception, ex:
            flash(_('Failed to update model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to update model')
            self.db.session.rollback()
            return False

    def delete_model(self):
        try:
            self.db.session.flush()
            self.db.session.delete(self.model)
            self.db.session.commit()
            return True
        except Exception, ex:
            flash(_('Failed to delete model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to delete model')
            self.db.session.rollback()
            return False


@hr.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("main.html")


@hr.route("/job/", methods=("GET", "POST"))
def job():
    data = Job.query.all()
    list_columns = ("job_name", "description")
    column_labels = dict(job_name=_("Job"), description=_("Description"))
    return render_template("list.html", model="job", list_columns=list_columns,
        column_labels=column_labels, data=data, count=0)


@hr.route("/job/view/id=<int:id>", methods=("GET", "POST"))
def job_view(id):
    return_url = request.args.get('next', url_for('.job'))

    job = Job.query.get(id)

    form = JobForm(next=return_url, obj=job)

    class FormAdmin(FormBase):
        fieldsets = [
            (None, {'fields': (('description', 'job_name'), ('job_name'))}),
            ('Other', {'fields': (('description', 'job_name'), )}),
            ('Addition', {'fields': ('job_name',)}),
        ]
        field_labels = dict(job_name=_("Job"), description=_("Description"))
    formadmin = FormAdmin(db, job, form, "job", return_url)

    return render_template("view.html", formadmin=formadmin,
        current_id=id)


@hr.route("/job/create/", methods=("GET", "POST"))
def job_create():
    return_url = request.args.get('next', url_for('.job'))

    job = Job()
    form = JobForm(next=return_url, obj=job)

    class FormAdmin(FormBase):
        readonly = False
        fieldsets = [
            (None, {'fields': ('job_name', 'description')}),
        ]
        field_labels = dict(job_name=_("Job"), description=_("Description"))
    formadmin = FormAdmin(db, job, form, "job", return_url)

    if formadmin.form.validate_on_submit():
        if formadmin.create_model():
            if '_add_another' in request.form:
                flash(_('Created successfully.'))
                return redirect(url_for('.job_create', url=return_url))
            else:
                return redirect(return_url)

    return render_template("create.html", formadmin=formadmin)


@hr.route("/job/edit/id=<int:id>/", methods=("GET", "POST"))
def job_edit(id):
    return_url = request.args.get('next', url_for('.job'))

    job = Job.query.get(id)
    form = JobForm(next=return_url, obj=job)

    class FormAdmin(FormBase):
        readonly = False
        fieldsets = [
            (None, {'fields': ('job_name', 'description')}),
        ]
        field_labels = dict(job_name=_("Job"), description=_("Description"))
    formadmin = FormAdmin(db, job, form, "job", return_url)

    if form.validate_on_submit():
        if formadmin.update_model():
            return redirect(return_url)

    return render_template("edit.html", formadmin=formadmin)


@hr.route("/job/delete/id=<int:id>/", methods=("GET", "POST"))
def job_delete(id):
    return_url = request.args.get('next', url_for('.job'))

    job = Job.query.get(id)

    class FormAdmin(FormBase):
        readonly = False
        fieldsets = [
            (None, {'fields': ('job_name', 'description')}),
        ]
        field_labels = dict(job_name=_("Job"), description=_("Description"))
    formadmin = FormAdmin(db, job, None, "job", return_url)

    if formadmin.model:
        formadmin.delete_model()

    return redirect(return_url)


@hr.route("/department/", methods=("GET", "POST"))
def department():
    data = Department.query.all()
    list_columns = ("dept_name", "description")
    column_labels = dict(dept_name=_("Department"),
        description=_("Description"))
    return render_template("list.html", model="department",
        list_columns=list_columns,
        column_labels=column_labels, data=data, count=0)


@hr.route("/department/id=<int:id>", methods=("GET", "POST"))
def department_view(id):
    return_url = request.args.get('next', url_for('.department'))

    department = Department.query.get(id)

    form = DepartmentForm(next=return_url, obj=department)

    class FormAdmin(FormBase):
        fieldsets = [
            (None, {'fields': ('dept_name', 'description')}),
        ]
        field_labels = dict(dept_name=_("Department"),
            description=_("Description"))
    formadmin = FormAdmin(db, department, form, "department", return_url)

    return render_template("view.html", formadmin=formadmin,
        current_id=id)


@hr.route("/department/create/", methods=("GET", "POST"))
def department_create():
    return_url = request.args.get('next', url_for('.department'))

    department = Department()
    form = DepartmentForm(next=return_url, obj=department)

    class FormAdmin(FormBase):
        readonly = False
        fieldsets = [
            (None, {'fields': ('dept_name', 'description')}),
        ]
        field_labels = dict(dept_name=_("Department"),
            description=_("Description"))
    formadmin = FormAdmin(db, department, form, "department", return_url)

    if formadmin.form.validate_on_submit():
        if formadmin.create_model():
            if '_add_another' in request.form:
                flash(_('Created successfully.'))
                return redirect(url_for('.department_create', url=return_url))
            else:
                return redirect(return_url)

    return render_template("create.html", formadmin=formadmin)


@hr.route("/department/edit/id=<int:id>/", methods=("GET", "POST"))
def department_edit(id):
    return_url = request.args.get('next', url_for('.department'))

    department = Department.query.get(id)
    form = DepartmentForm(next=return_url, obj=department)

    class FormAdmin(FormBase):
        readonly = False
        fieldsets = [
            (None, {'fields': ('dept_name', 'description')}),
        ]
        field_labels = dict(dept_name=_("Department"),
            description=_("Description"))
    formadmin = FormAdmin(db, department, form, "department", return_url)

    if form.validate_on_submit():
        if formadmin.update_model():
            return redirect(return_url)

    return render_template("edit.html", formadmin=formadmin)


@hr.route("/department/delete/id=<int:id>/", methods=("GET", "POST"))
def department_delete(id):
    return_url = request.args.get('next', url_for('.department'))

    department = Department.query.get(id)

    class FormAdmin(FormBase):
        fieldsets = [
            (None, {'fields': ('dept_name', 'description')}),
        ]
        field_labels = dict(dept_name=_("Department"),
            description=_("Description"))
    formadmin = FormAdmin(db, department, None, "department", return_url)

    if formadmin.model:
        formadmin.delete_model()

    return redirect(return_url)


# @hr.route("/employee/", methods=("GET", "POST"))
# def employee():
#     employee = Employee()
#     employee.query.all()
#     showfields = (("emp_code", _("Employee Code")),
#         ("emp_name", _("Employee")),
#         ("job", _("Job")), ("department", _("Department")),
#         ("level", _("Level")), ("manager", _("Manager")),
#         ("gender", _("Gender")), ("id_card", _("ID Card")))
#     return render_template("list.html", folder="hr", link="hr.employee",
#         showfields=showfields, table=employee.query.all())


# @hr.route("/employee/edit=<int:id>/", methods=("GET", "POST"))
# def employee_edit(id):
#     # is add
#     if id == 0:
#         employee = Employee()
#     # is edit
#     else:
#         employee = Employee().query.get(id)

#     form = EmployeeForm(next=request.args.get('next', None), obj=employee)

#     form.related_user.choices = [(0, "")]
#     form.related_user.choices.extend([(g.id, g.emp_name) for g in
#         Employee.query.filter_by(active=True).order_by('emp_name')])
#     form.department.choices = [(g.id, g.dept_name) for g in
#         Department.query.filter_by(active=True).order_by('dept_name')]
#     form.job.choices = [(g.id, g.job_name) for g in
#         Job.query.filter_by(active=True).order_by('job_name')]
#     form.gender_id.choices = [(g.item_id, g.item_name) for g in
#         Item.query.filter_by(active=True, group_id=1).order_by('item_id')]
#     form.marital_id.choices = [(g.item_id, g.item_name) for g in
#         Item.query.filter_by(active=True, group_id=2).order_by('item_id')]
#     form.manager.choices = [(0, "")]
#     form.manager.choices.extend([(g.id, g.emp_name) for g in
#         Employee.query.filter_by(active=True).order_by('emp_name')])

#     if form.validate_on_submit():
#         form.populate_obj(employee)
#         employee.save()

#         next_url = form.next.data
#         if not next_url or next_url == request.path:
#             next_url = url_for('hr.main')

#         return redirect(url_for('hr.employee'))

#     return render_template("hr/employee.html", form=form)


# @hr.route("/job/delete=<int:id>/", methods=("GET", "POST"))
# def employee_delete(id):
#     employee = Employee.query.get(id)
#     if employee:
#         employee.delete()
#     return redirect(url_for("hr.employee"))
