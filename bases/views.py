from flask import Blueprint, render_template
from flask.ext.babel import gettext as _
from flask_admin.contrib import sqlamodel
from flask_admin.model.form import InlineFormAdmin

from .models import ItemGroup, Item
from .forms import ItemGroupForm

from pyservice.extensions import db, admin
from pyservice.base import FormBase

bases = Blueprint('bases', __name__,
    url_prefix="/bases",
    static_folder='static')


@bases.route("/main/", methods=("GET", "POST"))
def main():
    return render_template("bases/main.html")


class ItemFormAdmin(InlineFormAdmin):
    form_columns = ('item_order', 'item_name')


class ItemGroupModelView(sqlamodel.ModelView):
    inline_models = (ItemFormAdmin(Item), )
    column_list = ('type_code', 'group_name', 'items')
    # form_columns = ('type_code', 'group_name', 'items')


admin.add_view(ItemGroupModelView(ItemGroup, db.session, name='Item',
    endpoint='itemgroup', category='Base'))


class ItemAdmin(FormBase):
    list_columns = ("item_order", "item_name")
    fieldsets = [
        (None, {'fields': ('item_order', 'item_name')}),
    ]
    column_labels = dict(item_order=_("Order"), item_name=_("Item Name"))


class ItemGroupAdmin(FormBase):
    list_columns = ("type_code", "group_name", 'items')
    fieldsets = [
        (None, {'fields': ('type_code', 'group_name', 'items', 'add_recipient')}),
    ]
    column_labels = dict(type_code=_("Type"), group_name=_("Group Name"))

itemgroupadmin = ItemGroupAdmin(bases, db.session, ItemGroup, ItemGroupForm)


@bases.route("/itemgroup/", methods=("GET", "POST"))
def itemgroup():
    return itemgroupadmin.list_view()


@bases.route("/itemgroup/view/id=<int:id>", methods=("GET", "POST"))
def itemgroup_view(id):
    return itemgroupadmin.show_view(id)


@bases.route("/itemgroup/create/", methods=("GET", "POST"))
def itemgroup_create():
    return itemgroupadmin.create_view()


@bases.route("/itemgroup/edit/id=<int:id>/", methods=("GET", "POST"))
def itemgroup_edit(id):
    return itemgroupadmin.edit_view(id)


@bases.route("/itemgroup/delete/id=<int:id>/", methods=("GET", "POST"))
def itemgroup_delete(id):
    return itemgroupadmin.delete_view(id)
