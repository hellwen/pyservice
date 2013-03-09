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
from flask.ext.admin.contrib import sqlamodel

from pyservice.extensions import db, admin
from pyservice.helpers import render_template
from pyservice.models import ItemGroup, Item

base = Module(__name__)

class ItemGroupAdmin(sqlamodel.ModelView):
    column_list = ('type_code', 'group_name')

    def create_model(self, form):
        """
            Create model from form.

            :param form:
                Form instance
        """
        try:
            model = self.model()
            form.populate_obj(model)
            model.group_name = model.group_name + "----create"
            self.session.add(model)
            self.on_model_change(form, model)
            self.session.commit()
            return True
        except Exception, ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            logging.exception('Failed to create model')
            self.session.rollback()
            return False

admin.add_view(ItemGroupAdmin(ItemGroup, db.session, name=_('Item Group'), endpoint='itemgroup', category=_('Base')))
