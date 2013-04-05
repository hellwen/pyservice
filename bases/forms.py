from flask.ext.wtf import Form, TextField, HiddenField, required,\
    FormField, FieldList, SubmitField
from flask.ext.babel import gettext as _


class ItemForm(Form):
    item_order = TextField(_("Item Order"), validators=[
        required(message=_("You must provide"))])
    item_name = TextField(_("Item Name"), validators=[
        required(message=_("You must provide"))])


class ItemGroupForm(Form):
    next = HiddenField()

    type_code = TextField(_("Type"), validators=[
        required(message=_("You must provide"))])
    group_name = TextField(_("Group Name"), validators=[
        required(message=_("You must provide"))])
    items = FieldList(FormField(ItemForm), min_entries=1)

    add_recipient = SubmitField()
