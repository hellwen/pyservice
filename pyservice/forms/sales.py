#!/usr/bin/env python
#coding=utf-8

"""
    forms: account.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, TextAreaField, HiddenField, BooleanField, SelectField, IntegerField, \
        PasswordField, SubmitField, TextField, DateTimeField, DateField, DecimalField, ValidationError, \
        required, email, equal_to, regexp

from flask.ext.babel import gettext, lazy_gettext as _ 

from pyservice.extensions import db
from pyservice.models import User

from .validators import is_username

class MountMendForm(Form):

    bill_type         = TextField(_("Bill Type"), validators=[required(message=_("You must provide an email or username"))])
    bill_flag         = IntegerField(_("Bill Flag"))
    self_code         = TextField(_("self_code"), validators=[required(message=_("You must provide an email or username"))])
    work_sheet_no     = TextField(_("Work No"))
    
    # 基本用户信息
    user_name         = TextField(_("Customer Name"), validators=[required(message=_("You must provide an email or username"))])
    user_tele         = TextField(_("Customer Telephone"))
    user_address      = TextField(_("Customer Address"))
    
    # 商品信息
    good_model        = TextField(_("Good Model"))
    good_code         = TextField(_("Good Code"))
    report_gz         = TextField(_("report_gz"))
    appearance        = TextField(_("Appearance"))
    accessory         = TextField(_("Accessory"))
    
    # 商品购买信息
    vendor            = TextField(_("Vendor"))
    buy_date          = DateTimeField(_("Buy Date"))
    invoice_no        = TextField(_("Invoice No"))
    ensure_no         = TextField(_("Ensure No"))
    
    # 收货信息
    receive_date      = DateTimeField(_("Receive Date"))
    apply_time_limit  = DateTimeField(_("Time Limit"))
    fetch_date        = DateTimeField(_("fetch_date"))
    mend_property_id  = SelectField(_("Mend Property"), default=0, coerce=int)
    user_type_id      = SelectField(_("user_type_id"), default=0, coerce=int)
    source_of_info_id = SelectField(_("Sources of Information"), default=0, coerce=int)

    receiver_id          = SelectField(_("Receiver"), default=0, coerce=int, validators=[required(message=_("You must choices a department"))])
    department_id     = SelectField(_("Department"), default=0, coerce=int, validators=[required(message=_("You must choices a department"))])

    remark            = TextField(_("Remark"))
    
    next              = HiddenField()
    
    submit            = SubmitField(_("Save"))

class MountMendFeedbackForm(Form):

    bill_type         = TextField(_("Bill Type"), validators=[required(message=_("You must provide an email or username"))])
    bill_flag         = IntegerField(_("Bill Flag"))
    self_code         = TextField(_("self_code"), validators=[required(message=_("You must provide an email or username"))])
    work_sheet_no     = TextField(_("Work No"))
    
    # 基本用户信息
    user_name         = TextField(_("Customer Name"), validators=[required(message=_("You must provide an email or username"))])
    user_tele         = TextField(_("Customer Telephone"))
    user_address      = TextField(_("Customer Address"))
    
    # 商品信息
    good_model        = TextField(_("Good Model"))
    good_code         = TextField(_("Good Code"))
    report_gz         = TextField(_("report_gz"))
    appearance        = TextField(_("Appearance"))
    accessory         = TextField(_("Accessory"))
    
    # 商品购买信息
    vendor            = TextField(_("Vendor"))
    buy_date          = DateTimeField(_("Buy Date"))
    invoice_no        = TextField(_("Invoice No"))
    ensure_no         = TextField(_("Ensure No"))
    
    # 收货信息
    receive_date      = DateTimeField(_("Receive Date"))
    apply_time_limit  = DateTimeField(_("Time Limit"))
    fetch_date        = DateTimeField(_("fetch_date"))
    mend_property_id  = SelectField(_("Mend Property"), default=0, coerce=int)
    user_type_id      = SelectField(_("user_type_id"), default=0, coerce=int)
    source_of_info_id = SelectField(_("Sources of Information"), default=0, coerce=int)

    receiver_id          = SelectField(_("Receiver"), default=0, coerce=int, validators=[required(message=_("You must choices a department"))])
    department_id     = SelectField(_("Department"), default=0, coerce=int, validators=[required(message=_("You must choices a department"))])

    # 维修信息
    shou_man_id          = SelectField(_("shou_man_id"), default=0, coerce=int)
    gz_reason         = TextField(_("gz_reason"))
    wx_deal           = TextField(_("wx_deal"))
    cq_reason         = TextField(_("cq_reason"))
    deal_type_id    = SelectField(_("deal_type_id"), default=0, coerce=int)
    mend_date         = DateTimeField(_("mend_date"))

    bx_mater          = TextField(_("bx_mater"))
    bx_mater_fee      = DecimalField(_("bx_mater_fee"), default=0)
    zf_mater          = TextField(_("zf_mater"))
    zf_mater_fee      = DecimalField(_("zf_mater_fee"))

    bx_gs             = IntegerField(_("bx_gs"))
    zf_gs             = IntegerField(_("bx_gs"))
    sm_gs             = IntegerField(_("sm_gs"))

    other_fee         = DecimalField(_("other_fee"))
    user_gs_fee       = DecimalField(_("user_gs_fee"))

    distance_km       = IntegerField(_("distance_km"))
    shou_car_flag     = IntegerField(_("shou_car_flag"))

    # 发件信息
    fj_emp_id            = SelectField(_("fj_emp_id"), default=0, coerce=int)

    fj_invoice        = TextField(_("fj_invoice"))
    fj_date           = DateTimeField(_("fj_date")) 

    remark            = TextField(_("Remark"))
    
    next              = HiddenField()
    
    submit            = SubmitField(_("Save"))