#!/usr/bin/env python
#coding:utf-8

"""
    todo.py
    ~~~~~~~~~~~~~~~
    
    简明Flask实现的TODO程序。

    :copyright: (c) 2011 by wwq0327 <wwq0327@gmail.com>
    :lecense: LGPL
"""
import os
from datetime import datetime

from flask import Flask, render_template, url_for, redirect, flash, request
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, SubmitField, required, ValidationError

## config
DEBUG = True
SECRET_KEY = '\xb5\xc8\xfb\x18\xba\xc7*\x03\xbe\x91{\xfd\xe0L\x9f\xe3\\\xb3\xb1P\xac\xab\x061'
SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.sqlite'

app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)
db.init_app(app)

manager = Manager(app)

@manager.command
def createall():
    '''创建数据库'''
    
    db.create_all()

@manager.command
def dropall():
    '''清除数据'''
    
    db.drop_all()

# 定义一个数据模型，相当于一个表
class Todo(db.Model):
    '''数据模型'''
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    posted_on = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.Boolean(), default=False)

    # 初始化
    def __init__(self, *args, **kwargs):
        super(Todo, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Todo '%s'>" % self.title

    # 数据操作方法
    def store_to_db(self):
        '''保存数据到数据库'''
        
        db.session.add(self)
        db.session.commit()

    def delete_todo(self):
        '''删除数据'''
        
        db.session.delete(self)
        db.session.commit()

    def validate_title(form, field):
        '''数据校验'''
        if field.data == 0:
            raise ValidationError, u'内容不能为空'
        return True

#  定义一个表单
class TodoForm(Form):
    '''表单'''
    
    title = TextField(u"内容", validators=[required(message=u"任务内容")])
    #submit = SubmitField(u"Add")

@app.route('/', methods=['GET', 'POST'])
def index():
    todo = Todo.query.order_by('-id')
    form = TodoForm(request.form)
    if request.method == 'POST':# and form.validate_on_submit():
        t = Todo(title=form.title.data)
        try:
            t.store_to_db()
            flash(u"添加成功")
            return redirect(request.args.get('next') or url_for('index'))
        except:
            flash(u'存储失败！')
            
    return render_template('index.html', todo=todo, form=form)

@app.route('/<int:id>/del')
def tdel(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        todo.delete_todo()
    flash(u"记录删除成功")
    return redirect(url_for('index'))

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.filter_by(id=id).first()
    form = TodoForm(title=todo.title)
    if request.method == 'POST':# and form.validate_on_submit():
        Todo.query.filter_by(id=id).update({Todo.title:request.form['title']})
        db.session.commit()
        flash(u"记录编辑成功")
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo, form=form)

@app.route('/<int:id>/done')
def done(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        Todo.query.filter_by(id=id).update({Todo.status:True})
        db.session.commit()
        flash(u"任务完成")

    return redirect(url_for('index'))

@app.route('/<int:id>/redo')
def redo(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        Todo.query.filter_by(id=id).update({Todo.status:False})
        flash(u"记录重置成功")
        db.session.commit()

    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_404.html'), 404

if __name__ == '__main__':
    app.run()
