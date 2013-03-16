from flask.ext.wtf import Form, TextField, HiddenField, required
from flask.ext.babel import gettext as _


class ItemGroupForm(Form):
    next = HiddenField()

    type_code = TextField(_("Type"), validators=[
        required(message=_("You must provide"))])
    group_name = TextField(_("Group Name"), validators=[
        required(message=_("You must provide"))])


class ItemForm(Form):
    next = HiddenField()

    item_order = TextField(_("Item Order"), validators=[
        required(message=_("You must provide"))])
    item_name = TextField(_("Item Name"), validators=[
        required(message=_("You must provide"))])
