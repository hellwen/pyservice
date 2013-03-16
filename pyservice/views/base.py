#! /usr/bin/env python
#coding=utf-8
"""
    base.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

from flask import Module, request, render_template, url_for, redirect
from flask.ext.babel import gettext as _

# from pyservice.models import Item
# from pyservice.forms import ItemForm

# base = Module(__name__)


# @base.route("/main/", methods=("GET", "POST"))
# def main():
#     return render_template("base/main.html")


# @base.route("/item/", methods=("GET", "POST"))
# def item():
#     data = Item.query.all()
#     list_columns = (("item_order", _("Item Order")),
#         ("item_name", _("Item Name")), ("group_id", _("Group ID")),
#         ("group_name", _("Group Name")))
#     return render_template("list.html", module="base", model="item",
#         list_columns=list_columns, data=data)


# @base.route("/item/edit=<int:id>/", methods=("GET", "POST"))
# def item_edit(id):
#     # is add
#     if id == 0:
#         item = Item()
#     # is edit
#     else:
#         item = Item.query.get(id)

#     form = ItemForm(next=request.args.get('next', None), obj=item)

#     if form.validate_on_submit():
#         form.populate_obj(item)
#         item.unique_id = item.group_id * 1000 + item.item_id
#         item.save()

#         next_url = form.next.data
#         if not next_url or next_url == request.path:
#             next_url = url_for('base.main')

#         return redirect(url_for('base.item'))

#     return render_template("base/item.html", form=form)


# @base.route("/item/delete=<int:id>/", methods=("GET", "POST"))
# def item_delete(id):
#     item = Item.query.get(id)
#     if item:
#         item.delete()
#     return redirect(url_for("base.item"))
