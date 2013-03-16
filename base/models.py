#!/usr/bin/env python
#coding=utf-8
"""
    models: bases.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime
from pyservice.extensions import db
import flask.ext.sqlalchemy

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, aliased
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

class ItemGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_code = db.Column(db.String(10), nullable=False)
    group_name = db.Column(db.String(30), nullable=False)
    items = db.relationship('Item', cascade="all, delete, delete-orphan", backref='item')
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.group_name

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(ItemGroup.id), nullable=False)
    item_id = db.Column(db.Integer, nullable=False, unique=True)
    _item_order = db.Column('item_order', db.Integer, default=0)
    item_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)

    @hybrid_property
    def item_order(self):
        return self._item_order

    @item_order.setter
    def item_order(self, value):
        self._item_order = value
        if self.group_id:
            self.item_id = self.group_id * 1000 + value

    # def _get_item_order(self):
    #     return self._item_order
    
    # def _set_item_order(self, value):
    #     self._item_order = self.group_id * 1000 + value
    
    # item_order = db.synonym("_item_order", 
    #                       descriptor=property(_get_item_order,
    #                                           _set_item_order))            

    def __unicode__(self):
        return self.item_name        