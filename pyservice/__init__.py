#!/usr/bin/env python
#coding=utf-8

"""
    __init__.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
import os
import logging
import datetime

from logging.handlers import SMTPHandler, RotatingFileHandler
from werkzeug import parse_date

from flask import Flask, g, session, request, flash, redirect, jsonify, url_for

from flask.ext.babel import Babel, gettext as _
from flask.ext.principal import Principal, RoleNeed, UserNeed, identity_loaded
from flask.ext.uploads import configure_uploads
from flask.ext.login import LoginManager, current_user

from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.admin import Admin, AdminIndexView, expose
import flask.ext.sqlalchemy
from pyservice import views, helpers
from pyservice.models import User
from pyservice.extensions import db, mail, cache, photos, restapi, login_manager, admin

DEFAULT_APP_NAME = 'pyservice'

DEFAULT_MODULES = (
    (views.frontend, ""),
    (views.sales, "/sales"),
    (views.hr, "/hr"),
    (views.base, "/base"),
    (views.account, "/account"),
    (views.footer, "/footer"),
)

def create_app(config=None, modules=None):

    if modules is None:
        modules = DEFAULT_MODULES   
    
    app = Flask(DEFAULT_APP_NAME)

    # config
    if config is not None:
        app.config.from_pyfile(config)
    
    configure_extensions(app)
    configure_login(app)

    configure_admin(app)
    configure_identity(app)
    configure_logging(app)
    configure_errorhandlers(app)
    configure_before_handlers(app)
    configure_template_filters(app)
    # configure_context_processors(app)
    configure_uploads(app, (photos,))

    configure_i18n(app)
    
    # register module
    configure_modules(app, modules) 

    return app

def configure_extensions(app):
    # configure extensions          
    db.init_app(app)
    # restapi.init_app(app, flask_sqlalchemy_db=db)
    # restapi.create_api(Job, collection_name="job", methods=['GET', 'POST', 'DELETE'])
    # restapi.create_api(Department, collection_name="department", methods=['GET', 'POST', 'DELETE'])
    mail.init_app(app)
    cache.init_app(app)
    toolbar = DebugToolbarExtension(app)

def configure_identity(app):

    principal = Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)

def configure_admin(app):

    # Create customized index view class
    class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            return current_user.is_authenticated()            

        # @expose('/')
        # def index(self):
        #     arg1 = 'Hello'
        #     return render_template('index.html', arg1=arg1)            

    admin.init_app(app)
    admin.name = DEFAULT_APP_NAME
    admin.index_view = MyAdminIndexView(url="/")

def configure_login(app):
    login_manager.setup_app(app)
    # login_manager.login_view = "login"
    # login_manager.login_message = u"Please log in to access this page."
    # login_manager.refresh_view = "reauth"

    @login_manager.user_loader
    def load_user(userid):
        return User.query.filter_by(id=userid).first()
        # return User.get(userid)

def configure_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES',['en','zh'])
        return request.accept_languages.best_match(accept_languages)


def configure_context_processors(app):

    @app.context_processor
    def tags():
        tags = cache.get("tags")
        if tags is None:
            tags = Tag.query.cloud()
            cache.set("tags", tags)
        return dict(tags=tags)    

    @app.context_processor
    def links():
        links = cache.get("links")
        if links is None:
            links = Link.query.filter(Link.passed==True).limit(10).all()
            cache.set("links", links)
        return dict(links=links)    

    @app.context_processor
    def archives():
        archives = cache.get("archives")
        if archives is None:
            begin_post = Post.query.order_by('created_date').first()
            
            now = datetime.datetime.now()

            begin = begin_post.created_date if begin_post else now
            end = now

            total = (end.year-begin.year)*12 - begin.month + end.month
            archives = [begin]

            date = begin
            for i in range(total):
                if date.month<12: 
                    date = datetime.datetime(date.year,date.month+1,1)
                else:
                    date = datetime.datetime(date.year+1, 1, 1)
                archives.append(date)
            archives.reverse()
            cache.set("archives", archives)
        
        return dict(archives=archives)

    @app.context_processor
    def latest_comments():
        latest_comments = cache.get("latest_comments")
        if latest_comments is None:
            latest_comments = Comment.query.order_by(Comment.created_date.desc()) \
                                           .limit(5).all()
            cache.set("latest_comments", latest_comments)
        return dict(latest_comments=latest_comments)    

    @app.context_processor
    def config():
        return dict(config=app.config)


def configure_template_filters(app):
    
    @app.template_filter()
    def timesince(value):
        return helpers.timesince(value)

    @app.template_filter()
    def endtags(value):
        return helpers.endtags(value)

    @app.template_filter()
    def gravatar(email,size):
        return helpers.gravatar(email,size)

    @app.template_filter()
    def format_date(date,s='full'):
        return helpers.format_date(date,s)

    @app.template_filter()
    def format_datetime(time,s='full'):
        return helpers.format_datetime(time,s)

    @app.template_filter()
    def twitter_date(date):
        return parse_date(date)
    
    @app.template_filter()
    def code_highlight(html):
        return helpers.code_highlight(html)

    @app.template_filter()
    def gistcode(html):
        return helpers.gistcode(html)


def configure_before_handlers(app):

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)


def configure_errorhandlers(app):
    
    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonfiy(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))
  
    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not allowed'))
        return helpers.render_template("errors/403.html", error=error)

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return helpers.render_template("errors/404.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return helpers.render_template("errors/500.html", error=error)


def configure_modules(app, modules):
    
    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)


def configure_logging(app):

    mail_handler = \
        SMTPHandler(app.config['MAIL_SERVER'],
                    app.config['DEFAULT_MAIL_SENDER'],
                    app.config['ADMINS'], 
                    'application error',
                    (
                        app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'],
                    ))

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path, 
                             app.config['DEBUG_LOG'])

    debug_file_handler = \
        RotatingFileHandler(debug_log,
                            maxBytes=100000,
                            backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, 
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)