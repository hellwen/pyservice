#! /usr/bin/env python
#coding=utf-8
from flask.ext.principal import RoleNeed, Permission

admin_permission = Permission(RoleNeed('admin'))

# this is assigned when you want to block a permission to all
# never assign this role to anyone !
null = Permission(RoleNeed('null'))
