#! /usr/bin/env python
#coding=utf-8
"""
    base.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import datetime
import os, sys

import logging
from flask import Module, flash
from flask.ext.babel import gettext as _
from flask.ext import wtf
from flask.ext.admin.contrib import sqlamodel
from flask.ext.admin.contrib.sqlamodel import form


from pyservice.extensions import db, admin
from pyservice.helpers import render_template
from pyservice.models import ItemGroup, Item

base = Module(__name__)

class ItemAdmin(sqlamodel.ModelView):
    form_columns = ('group', 'item_order', 'item_name')
    column_list = ('group', 'item_order', 'item_name')
    column_labels = dict(group=_('Group'), item_order=_('Item Order'), item_name=_('Item Name'))

    def on_model_change(self, form, model):
        logging.warning(model.item_order)
        model.item_id = 1000 + model.item_order

admin.add_view(ItemAdmin(Item, db.session, name=_('Item'), endpoint='item', category=_('Base')))

ITEMTYPE_CHOICES = (
    ('hr', _('HR')),
    ('wo', _('WorkOrder')),
)

class ItemGroupAdmin(sqlamodel.ModelView):
    # inline_models = (ItemAdmin(Item),)

    form_columns = ('type_code', 'group_name')
    column_list = ('type_code', 'group_name')
    column_labels = dict(type_code=_('Type'), group_name=_('Group Name'))    

    form_overrides = dict(type_code=wtf.SelectField)
    form_args = dict(
            type_code=dict(choices=ITEMTYPE_CHOICES)
        )    

admin.add_view(ItemGroupAdmin(ItemGroup, db.session, name=_('Item Group'), endpoint='itemgroup', category=_('Base')))
