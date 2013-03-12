#!/usr/bin/env python
#coding=utf-8

"""
    __init__.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, request, flash, redirect, jsonify, url_for

from flask.ext.babel import Babel, gettext as _
# from flask_debugtoolbar import DebugToolbarExtension

from pyservice import views, helpers
from pyservice.extensions import db, cache

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
    configure_errorhandlers(app)
    configure_i18n(app)

    # register module
    configure_modules(app, modules)

    return app


def configure_extensions(app):
    # configure extensions
    db.init_app(app)
    # restapi.init_app(app, flask_sqlalchemy_db=db)
    # restapi.create_api(Job, collection_name="job",
    #     methods=['GET', 'POST', 'DELETE'])
    # restapi.create_api(Department, collection_name="department",
    #     methods=['GET', 'POST', 'DELETE'])
    cache.init_app(app)
    # toolbar = DebugToolbarExtension(app)


def configure_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES', ['en', 'zh'])
        return request.accept_languages.best_match(accept_languages)


def configure_errorhandlers(app):

    @app.errorhandler(401)
    def unauthorized(error):
        # if request.is_xhr:
        #     return jsonfiy(error=_("Login required"))
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
