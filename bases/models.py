from pyservice.extensions import db

from sqlalchemy import Column, Integer
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


class ItemGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_code = db.Column(db.String(10), nullable=False)
    group_name = db.Column(db.String(30), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.group_name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(ItemGroup.id),
        nullable=False)
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

    def __unicode__(self):
        return self.item_name
