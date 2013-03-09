#! /usr/bin/env python
#coding=utf-8
"""
    base.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import datetime
import os, sys

from flask import Module
from flask.ext.babel import gettext as _
from flask.ext import wtf

from pyservice.extensions import db
from pyservice.helpers import render_template
from pyservice.models import ItemGroup, Item

base = Module(__name__)

@base.route("/main/", methods=("GET","POST"))
def main():
    return render_template("base/main.html")

@base.route("/item/", methods=("GET","POST"))
def item():
    item = Item()
    showfields = (("item_id", _("Item Id")), ("item_order", _("Item Order")), ("item_name", _("Item Name")), ("group_id", _("Group ID")), ("group_name", _("Group Name")))
    return render_template("list.html", folder="hr", link="hr.item", showfields=showfields, table=item.joinall())

@base.route("/item/edit=<int:id>/", methods=("GET","POST"))
def item_edit(id):
    # is add
    if id==0:
        item = Item()
    # is edit
    else:
        item = Item.query.get(id)

    form = ItemForm(next=request.args.get('next',None), obj=item)

    if form.validate_on_submit():
        form.populate_obj(item)
        item.unique_id = item.group_id * 1000 + item.item_id
        item.save()

        next_url = form.next.data
        if not next_url or next_url == request.path:
            next_url = url_for('base.main')

        return redirect(url_for('base.item'))

    return render_template("base/item.html", form=form)

@base.route("/item/delete=<int:id>/", methods=("GET","POST"))
def item_delete(id):
    item = Item.query.get(id)
    if item:
        item.delete()
    return redirect(url_for("base.item"))