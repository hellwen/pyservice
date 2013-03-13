#! /usr/bin/env python
#coding=utf-8
"""
    sales.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""
import datetime

from flask import Blueprint, request, redirect, url_for, render_template

from flaskext.babel import gettext as _

from pyservice.models import MountMend, Employee, Item, Department
from pyservice.forms import MountMendForm, MountMendFeedbackForm

sales = Blueprint('sales', __name__)


@sales.route("/main", methods=("GET", "POST"))
def main():
    return render_template("sales/main.html")


@sales.route("/order", methods=("GET", "POST"))
def order():
    mountmend = MountMend()
    showfields = (("bill_type", _("Bill Type")), ("self_code", _("Self Code")),
        ("work_sheet_no", _("Work No")), ("user_name", _("Customer Name")),
        ("user_tele", _("Customer Telephone")),
        ("user_address", _("Customer Address")),
        ("good_model", _("Good Model")),
        ("good_code", _("Good Code")))
    return render_template("list.html", folder="sales", link="sales.order",
        showfields=showfields, table=mountmend.joinall())


@sales.route("/order/edit=<int:id>/", methods=("GET", "POST"))
def order_edit(id):
    # is add
    if id == 0:
        mountmend = MountMend()
        mountmend.bx_mater_fee = 0
        mountmend.receive_date = datetime.datetime.now()
        mountmend.apply_time_limit = mountmend.receive_date + \
            datetime.timedelta(days=3)
        mountmend.buy_date = datetime.datetime.now()

        mountmend.receiver_id = 1  # 当前用户
        # 当前用户所在的部门
        mountmend.department_id = \
            Employee.query.get(mountmend.receiver_id).department

        mountmend.bill_flag = 0
    # is edit
    else:
        mountmend = MountMend().query.get(id)

    form = MountMendForm(next=request.args.get('next', None), obj=mountmend)

    form.receiver_id.choices = [(g.id, g.emp_name) for g in
        Employee.query.filter_by(active=True).order_by('emp_name')]
    form.department_id.choices = [(g.id, g.dept_name) for g in
        Department.query.filter_by(active=True).order_by('dept_name')]

    form.mend_property_id.choices = [(g.item_id, g.item_name) for g in
        Item.query.filter_by(active=True, group_id=20).order_by('item_order')]
    form.user_type_id.choices = [(g.item_id, g.item_name) for g in
        Item.query.filter_by(active=True, group_id=23).order_by('item_order')]
    form.source_of_info_id.choices = [(g.item_id, g.item_name) for g in
        Item.query.filter_by(active=True, group_id=21).order_by('item_order')]

    if form.validate_on_submit():
        form.populate_obj(mountmend)
        mountmend.save()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('sales.main')

        return redirect(url_for('sales.order'))

    return render_template("sales/order.html", form=form)


@sales.route("/order/delete=<int:id>/", methods=("GET", "POST"))
def order_delete(id):
    mountmend = MountMend.query.get(id)
    if mountmend:
        mountmend.delete()
    return redirect(url_for("sales.order"))


@sales.route("/feedback", methods=("GET", "POST"))
def feedback():
    mountmend = MountMend()
    showfields = (("bill_type", _("Bill Type")), ("self_code", _("Self Code")),
        ("work_sheet_no", _("Work No")), ("user_name", _("Customer Name")),
        ("user_tele", _("Customer Telephone")),
        ("user_address", _("Customer Address")),
        ("good_model", _("Good Model")),
        ("good_code", _("Good Code")))
    return render_template("sales/feedback_list.html", folder="sales",
        link="sales.feedback", showfields=showfields, table=mountmend.joinall())


@sales.route("/feedback/edit=<int:id>/", methods=("GET", "POST"))
def feedback_edit(id):
    # only edit, not add
    mountmend = MountMend().query.get(id)
    mountmend.bx_mater_fee = 0
    mountmend.zf_mater_fee = 0
    mountmend.bx_gs = 0
    mountmend.zf_gs = 0
    mountmend.sm_gs = 0
    mountmend.other_fee = 0
    mountmend.user_gs_fee = 0
    mountmend.distance_km = 0

    mountmend.mend_date = datetime.datetime.now()
    mountmend.fj_date = datetime.datetime.now()

    form = MountMendFeedbackForm(next=request.args.get('next', None),
        obj=mountmend)

    form.receiver_id.choices = [(g.id, g.emp_name) for g in
        Employee.query.filter_by(active=True).order_by('emp_name')]
    form.department_id.choices = [(g.id, g.dept_name) for g in
        Department.query.filter_by(active=True).order_by('dept_name')]

    form.mend_property_id.choices = [(g.item_id, g.item_name) for g in
        Item.query.filter_by(active=True, group_id=20).order_by('item_order')]
    form.user_type_id.choices = [(g.item_id, g.item_name) for g in
        Item.query.filter_by(active=True, group_id=23).order_by('item_order')]
    form.source_of_info_id.choices = [(g.item_id, g.item_name) for g in
        Item.query.filter_by(active=True, group_id=21).order_by('item_order')]

    form.shou_man_id.choices = [(0, "")]
    form.shou_man_id.choices.extend([(g.id, g.emp_name) for g in
        Employee.query.filter_by(active=True).order_by('emp_name')])
    form.fj_emp_id.choices = [(0, "")]
    form.fj_emp_id.choices.extend([(g.id, g.emp_name) for g in
        Employee.query.filter_by(active=True).order_by('emp_name')])

    form.deal_type_id.choices = [(g.item_id, g.item_name) for g in
        Item.query.filter_by(active=True, group_id=22).order_by('item_order')]

    if form.validate_on_submit():
        form.populate_obj(mountmend)
        mountmend.save()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('sales.main')

        return redirect(url_for('sales.feedback'))

    return render_template("sales/feedback.html", form=form)
