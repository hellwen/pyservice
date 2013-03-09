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
    group = db.relationship('ItemGroup', foreign_keys=group_id, backref='itemgoup')
    item_id = db.Column(db.Integer, nullable=False, unique=True)
    item_order = db.Column(db.Integer, default=0)
    item_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.item_name        