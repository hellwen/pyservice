#!/usr/bin/env python
#coding=utf-8
"""
    models: users.py
    ~~~~~~~~~~~~~
    :license: BSD, see LICENSE for more details.
"""

import hashlib

from datetime import datetime

from werkzeug import cached_property

from flask import abort, current_app

from flask.ext.sqlalchemy import BaseQuery
from flask.ext.principal import RoleNeed, UserNeed, Permission

from pyservice.extensions import db, cache
from pyservice.permissions import admin


class MountMend(db.Model):

    __tablename__          = 'mountmends'

    id                     = db.Column(db.Integer, primary_key=True)
    bill_type              = db.Column(db.Integer) # 安装、维修、调试、送货/安装
    bill_flag              = db.Column(db.Integer)
    # send_no              = db.Column(db.String(18)) 
    self_code              = db.Column(db.String(30), unique=True, nullable=False) # 接收单号
    
    department_id          = db.Column(db.Integer)   # 接收部门
    # department             = db.relationship("Department", foreign_keys=department_id, remote_side=id)
    
    # goods_code           = db.Column(db.Integer)) 详见 pmxh
    good_model             = db.Column(db.String(255))  # 品牌型号
    
    user_name              = db.Column(db.String(50), nullable=False)  #  用户名称
    user_tele              = db.Column(db.String(50))  #  用户电话
    user_address           = db.Column(db.String(100))  #  用户地址
    # User_areaCode        = db.Column(db.String(50))
    
    # pmxh                 = db.Column(db.String(255))  品牌型号，如果是选择则为空采用goods_code并在这里显示名称，如果是填写这使用该字段
    
    # number               = db.Column(db.Integer))
    
    buy_date               = db.Column(db.DateTime)  # 购机日期
    # out_fact_date        = db.Column(db.datetim))  
    # invoice                = db.Column(db.String(50))   # 发票号
    invoice_no                = db.Column(db.String(50))   # 发票号
    
    # spbh                 = db.Column(db.String(1024))  # 商品编号
    good_code              = db.Column(db.String(100))
    
    report_gz              = db.Column(db.String(512))   # 故障原因
    vendor                 = db.Column(db.String(50))    # 销售单位
    # rece_date              = db.Column(db.Date))  # 接件时间
    receive_date              = db.Column(db.DateTime)  # 接件时间
    # rece_man               = db.Column(db.String(20))  # 接件员
    receiver_id          = db.Column(db.Integer)  # 接件员
    apply_time_limit       = db.Column(db.DateTime)  # 要求期限
    # apply_date           = db.Column(db.Date))
    fetch_date             = db.Column(db.DateTime)   # 预约时间
    # info_code            = db.Column(db.String(40))   # 信息来源
    source_of_info_id      = db.Column(db.Integer)   # 信息来源
    # deal_mode            = db.Column(db.String(50))   # 处理方式
    # wx_attr              = db.Column(db.String(2))      # 服务性质
    mend_property_id       = db.Column(db.Integer)    # 服务性质
    # pdaz_date            = db.Column(db.Date))    # 只见在备注中的日期吻合
    # send_man             = db.Column(db.String(20))
    # fetch_man            = db.Column(db.String(20))
    # send_fee             = db.Column(db.Numeric(8,2)))
    # fetch_fee            = db.Column(db.Numeric(8,2)))
    shou_man_id               = db.Column(db.String(20))    # 收件员
    gz_reason              = db.Column(db.String(100))  # 故障原因
    wx_deal                = db.Column(db.String(100))  # 维修措施
    cq_reason              = db.Column(db.String(100))  # 超期原因
    # cq_first_date        = db.Column(db.Date))   # 应该是超期时间，但不知道在哪里使用
    # cq_last_date         = db.Column(db.Date))
    mend_date              = db.Column(db.DateTime)    # 完工日期
    # in_mend_date         = db.Column(db.Date)) 
    bx_mater               = db.Column(db.String(300))  # 保修材料
    bx_mater_fee           = db.Column(db.Numeric(8,2))    # 保修材料费
    zf_mater               = db.Column(db.String(300))  # 自费材料
    zf_mater_fee           = db.Column(db.Numeric(8,2))    # 自费材料费
    
    # deal_type_code         = db.Column(db.Integer))   #  措施类别
    deal_type_id         = db.Column(db.Integer)   #  措施类别
    # deal_type            = db.Column(db.String(18))   # 新增加
    
    
    # gs_fee               = db.Column(db.Numeric(8,2)))
    bx_gs                  = db.Column(db.Integer)  # 保修工时
    zf_gs                  = db.Column(db.Integer)  # 自费工时
    sm_gs                  = db.Column(db.Integer)  # 上门工时
    other_fee              = db.Column(db.Numeric(8,2))  # 杂项提成
    # other_in_fee         = db.Column(db.Numeric(8,2)))
    # trip_fee             = db.Column(db.Numeric(8,2)))
    
    # balance_fee          = db.Column(db.Numeric(8,2)))      # 费用合计  (为计算处理中所有费用总和)
    
    # fj_man                 = db.Column(db.String(20))       # 发件人
    fj_emp_id                 = db.Column(db.String(20))       # 发件人
    fj_invoice             = db.Column(db.String(18))   # 发件票号
    fj_date                = db.Column(db.DateTime)        # 发件时间
    remark                 = db.Column(db.String(300))
    # bala_flag            = db.Column(db.Integer)
    # redu_reason          = db.Column(db.String(50))   # 有小部分内容，未见哪里显示
    # redu_je              = db.Column(db.Numeric(8,2))
    # hf_result            = db.Column(db.String(10))    # 回访结果
    # hf_time1             = db.Column(db.Date)
    # hf_man1              = db.Column(db.String(20))
    # hf_list1             = db.Column(db.String(8))
    # hf_result1           = db.Column(db.String(1))
    # hf_time2             = db.Column(db.Date)
    # hf_man2              = db.Column(db.String(20))
    # hf_list2             = db.Column(db.String(8))
    # hf_result2           = db.Column(db.String(1))
    # hf_time3             = db.Column(db.Date))
    # hf_man3              = db.Column(db.String(20))
    # hf_list3             = db.Column(db.String(8))
    # hf_result3           = db.Column(db.String(1))
    user_gs_fee            = db.Column(db.Numeric(18, 2))  # 收用户费
    # shou_car_time        = db.Column(db.Date)    # 收卡时间
    # pp_self_code         = db.Column(db.String(18))   # 小部分有内容，未见显示
    # ori_mount_mend_dep   = db.Column(db.String(50))
    
    # user_type            = db.Column(db.String(18))  # 用户类型
    user_type_id           = db.Column(db.Integer(18))  # 用户类型：普通用户、延保用户
    
    # pm_type              = db.Column(db.String(50))
    # in_rece_date         = db.Column(db.Date)   # 只有备注中有相同日期
    distance_km            = db.Column(db.Integer)  # 公里数
    work_sheet_no          = db.Column(db.String(18))    # 工作单号
    
    # 结算处理
    # mount_mend_fee       = db.Column(db.Numeric(8,2))  # 安装维修费
    # car_allowance_fee    = db.Column(db.Numeric(8,2))  # 汽车铺贴
    # sm_fee               = db.Column(db.Numeric(8,2))             # 上门费
    # traffic_fee          = db.Column(db.Numeric(8,2))        # 交通费
    # hotel_fee            = db.Column(db.Numeric(8,2))          # 住宿费
    # man_allowance_fee    = db.Column(db.Numeric(8,2))  # 误工补贴
    # other_bala_fee       = db.Column(db.Numeric(8,2))     # 其他费用
    # transfer_fee         = db.Column(db.Numeric(8,2))       # 搬运费
    # info_fee             = db.Column(db.Numeric(8,2))           # 信息费
    
    # send_flag            = db.Column(db.Integer)
    shou_car_flag          = db.Column(db.Integer)      # 收卡状态
    # print_num            = db.Column(db.int)   # 估计是打印次数
    ensure_no              = db.Column(db.String(30))  # 保修证号
    # bala_process         = db.Column(db.Integer)
    # plan_man             = db.Column(db.String(20))   # 部分有内容，未见显示
    # tele_area_code       = db.Column(db.String(18))  # 电话区号，不知道在哪里显示
    accessory              = db.Column(db.String(50))  # 随机附件
    appearance             = db.Column(db.String(50))   # 机器外观
    # synch_flag  # 新增加
    # pm_class             = db.Column(db.String(18))
    # buy_price            = db.Cllumn(db.Numeric(8,2))
    # place_no             = db.Column(db.String(30))
    # mount_mend_gain_rate = db.Column(numeric(18, 2))
    # mater_gain_rate      = db.Column(numeric(18, 2))
    # self_def1            = db.Column(db.String(50))
    # self_def2            = db.Column(db.String(50))
    # self_def3            = db.Column(db.String(50))
    # self_def4            = db.Column(db.String(50))
    # self_def5            = db.Column(db.String(1024))
    # self_def6            = db.Column(float)
    # self_def7            = db.Column(float)
    # self_def8            = db.Column(Datetime)
    # self_def9            = db.Column(Datetime)
    # send_time            = db.Column(Datetime)
    # check_man            = db.Column(db.String(20))
    # check_date           = db.Column(Datetime)
    # rece_user_fee        = db.Column(Numeric(8,2))
    # client_id            = db.Column(int)
    
    # 结算处理
    # return_money(8,2)    = db.Column(Numeric(8,2))    # 返利金额
    
    # goods_picture        = db.Column(image)   # 维修图片
    
    # fz_flag              = db.Column(Integer)
    # no_check_reason      = db.Column(db.String(100))
    # print_date           = db.Column(Datetime)    # 打印日期
    # store_name           = db.Column(db.String(100))
    # paiche_time          = db.Column(Datetime)
    # app_arrival_time     = db.Column(Datetime)
    # end_chu_li_date      = db.Column(Datetime)
    # datacome_flag        = db.Column(int)

    def joinall(self):
        return db.session.execute(" \
            select id, bill_type, self_code, work_sheet_no, user_name, user_tele, user_address, good_model, good_code \
            from mountmends \
            ")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# class MountMendFeeRateSet(db.Model):

#     __tablename__ = 'mountmendfeeratesets'
    
#     id = db.Column(db.Integer, primary_key=True)
#     mountmend_id = db.Column(db.Integer, unique=True)
#     deal_type_code = db.Column(db.Integer, unique=True)
#     mount_mend_fee = db.Column(db.Numeric(8,2) NOT)
#     balance_fee = db.Column(db.Numeric(8,2))
#     fee_flag = db.Column(db.Integer)
#     km_allowance = db.Column(db.Numeric(8,2))
#     self_fee = db.Column(db.Numeric(8,2))
#     other_fee1 = db.Column(db.Numeric(8,2))
#     other_js_fee1 = db.Column(db.Numeric(8,2))
#     other_fee2 = db.Column(db.Numeric(8,2))
#     other_js_fee2 = db.Column(db.Numeric(8,2))
#     other_fee3 = db.Column(db.Numeric(8,2))
#     other_js_fee3 = db.Column(db.Numeric(8,2))
#     mount_mend_fee1 = db.Column(db.Numeric(8,2))
#     mount_mend_fee2 = db.Column(db.Numeric(8,2))
#     mount_mend_fee3 = db.Column(db.Numeric(8,2))


class MountMendMan(db.Model):

    __tablename__ = 'mountmendmans'

    id = db.Column(db.Integer, primary_key=True)
    mountmend_id = db.Column(db.Integer, unique=True)
    employee_id = db.Column(db.String(20), unique=True)

    man_flag = db.Column(db.Integer)
    tcbl = db.Column(db.Numeric(8, 2))
    gs_fee = db.Column(db.Numeric(8,2))
    bx_gs_fee = db.Column(db.Numeric(8,2))
    zf_gs_fee = db.Column(db.Numeric(8,2))

    def joinall(self):
        return db.session.execute(" \
            select id, group_id, group_name, item_id, item_order, item_name \
            from items \
            where active = 1 \
            order by group_id, item_order \
            ")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()    

