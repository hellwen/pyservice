#!/usr/bin/env python
#coding=utf-8

import uuid

from flask import Flask, current_app
from flask.ext.script import Server, Shell, Manager, Command, prompt_bool

from pyservice import create_app
from pyservice.extensions import db
from pyservice.models import Item

manager = Manager(create_app('config.cfg'))

manager.add_command("runserver", Server('0.0.0.0',port=8080))

def _make_context():
    return dict(db=db)
manager.add_command("shell", Shell(make_context=_make_context))

@manager.command
def createall():
    "Creates database tables"
    db.create_all()
    # db.session.execute(" \
    #         create unique index idx_items on items(group_id, item_id) \
    #         ")

@manager.command
def dropall():
    "Drops all database tables"
    
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

@manager.command
def initialize():
    "Initialize base information"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        # db.drop_all()
        # db.create_all()

        # 
        db.session.execute("delete from items")
        db.session.add(Item(1, u'性别', 1001, 1, u'男'))
        db.session.add(Item(1, u'性别', 1002, 2, u'女'))
        db.session.add(Item(2, u'婚姻状况', 2001, 1, u'单身'))
        db.session.add(Item(2, u'婚姻状况', 2002, 2, u'已婚'))
        db.session.add(Item(2, u'婚姻状况', 2003, 3, u'离异'))

        # 维修工单
        db.session.add(Item(20, u'服务性质', 20001, 1, u'自费'))
        db.session.add(Item(20, u'服务性质', 20002, 2, u'保修'))
        db.session.add(Item(20, u'服务性质', 20003, 3, u'返修'))
        db.session.add(Item(20, u'服务性质', 20004, 4, u'自费不结算'))
        db.session.add(Item(20, u'服务性质', 20005, 5, u'自费待收费'))
        db.session.add(Item(20, u'服务性质', 20006, 6, u'保修不结算'))
        db.session.add(Item(20, u'服务性质', 20007, 7, u'保修待收费'))
        db.session.add(Item(20, u'服务性质', 20008, 8, u'过保减免'))
        db.session.add(Item(20, u'服务性质', 20009, 9, u'顾客不接受'))
        db.session.add(Item(20, u'服务性质', 20010, 10, u'用户咨询'))
        db.session.add(Item(20, u'服务性质', 20011, 11, u'已不需要处理'))
        db.session.add(Item(20, u'服务性质', 20012, 12, u'暂不确定'))
        db.session.add(Item(21, u'信息来源', 21001, 1, u'用户送修'))
        db.session.add(Item(21, u'信息来源', 21002, 2, u'电话接单'))
        db.session.add(Item(21, u'信息来源', 21003, 3, u'站内载机'))
        db.session.add(Item(21, u'信息来源', 21004, 4, u'800转单'))
        db.session.add(Item(21, u'信息来源', 21005, 5, u'400转单'))
        db.session.add(Item(21, u'信息来源', 21006, 6, u'广州转单'))
        db.session.add(Item(21, u'信息来源', 21007, 7, u'商场报单'))
        db.session.add(Item(21, u'信息来源', 21008, 8, u'商场送修'))
        db.session.add(Item(22, u'措施类别', 22001, 1, u'等回复'))
        db.session.add(Item(22, u'措施类别', 22002, 2, u'等零件'))
        db.session.add(Item(22, u'措施类别', 22003, 3, u'其它原因'))
        db.session.add(Item(22, u'措施类别', 22004, 4, u'QC'))
        db.session.add(Item(22, u'措施类别', 22005, 5, u'故障不稳定'))
        db.session.add(Item(22, u'措施类别', 22006, 6, u'中修'))
        db.session.add(Item(22, u'措施类别', 22007, 7, u'修复'))
        db.session.add(Item(22, u'措施类别', 22008, 8, u'送修工厂'))
        db.session.add(Item(22, u'措施类别', 22009, 9, u'在3'))
        db.session.add(Item(22, u'措施类别', 22010, 10, u'在4'))
        db.session.add(Item(22, u'措施类别', 22011, 11, u'在5'))
        db.session.add(Item(22, u'措施类别', 22012, 12, u'指导使用'))
        db.session.add(Item(23, u'用户类型', 23001, 1, u'普通用户'))
        db.session.add(Item(23, u'用户类型', 23002, 2, u'延保用户'))

        db.session.commit()

@manager.command
def createadmin():
    "Create admin and password is admin"
    admin = User("admin", "admin", "admin@example.com", User.ADMIN)
    admin.password = "admin"
    db.session.add(admin)
    db.session.commit()

@manager.option('-r', '--role', dest='role', default="member")
@manager.option('-n', '--number', dest='number', default=1, type=int)
def createcode(role, number):
    codes = []
    usercodes = []
    for i in range(number):
        code = unicode(uuid.uuid4()).split('-')[0]
        codes.append(code)
        usercode = UserCode()
        usercode.code = code
        if role == "admin":
            usercode.role = User.ADMIN
        elif role == "moderator":
            usercode.role = User.MODERATOR
        else:
            usercode.role = User.MEMBER
        usercodes.append(usercode)
    if number==1:
        db.session.add(usercode)
    else:
        db.session.add_all(usercodes)
    db.session.commit()
    print "Sign up code:"
    for i in codes:
        print i
    return


if __name__ == "__main__":
    manager.run()
