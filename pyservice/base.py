import logging

from flask import request, redirect, url_for, render_template, flash
from flask.ext.babel import gettext as _


class FormBase(object):
    fieldsets = []
    column_labels = dict()
    readonly = False
    set_focus = True
    inline_models = None

    def __init__(self, blueprint, session, model, form_class):
        self.blueprint = blueprint
        self.session = session
        self.model = model
        self.form_class = form_class
        self.endpoint = model.__name__.lower()

    def get_field_categorys(self):
        return [(tab[0]) for tab in self.fieldsets if tab[0]]

    def is_tuple(self, field):
        return isinstance(field, tuple)

    def get_fields(self, category_name):
        for tab in self.fieldsets:
            if tab[0] == category_name and tab[1]['fields']:
                return tab[1]['fields']

    def get_form(self):
        pass

    def after_create_form(self, form):
        pass

    def create_form(self, next, obj):
        form = self.get_form()
        if not form:
            form = self.form_class(next=next, obj=obj)
        self.after_create_form(form)
        return form

    def create_model(self, obj):
        try:
            self.form.populate_obj(obj)
            self.session.add(obj)
            self.session.commit()
            return True
        except Exception, ex:
            flash(_('Failed to create model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to create model')
            self.session.rollback()
            return False

    def update_model(self, obj):
        try:
            self.form.populate_obj(obj)
            self.session.commit()
            return True
        except Exception, ex:
            flash(_('Failed to update model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to update model')
            self.session.rollback()
            return False

    def delete_model(self, obj):
        try:
            self.session.flush()
            self.session.delete(obj)
            self.session.commit()
            return True
        except Exception, ex:
            flash(_('Failed to delete model. %(error)s', error=str(ex)),
                'error')
            logging.exception('Failed to delete model')
            self.session.rollback()
            return False

    def list_view(self):
        self.data = self.model.query.all()
        self.count = 0
        return render_template("list.html", formadmin=self)

    def show_view(self, id):
        self.readonly = True
        self.return_url = request.args.get('next',
            url_for('.' + self.endpoint))

        obj = self.model.query.get(id)
        self.form = self.create_form(next=self.return_url, obj=obj)

        return render_template("view.html", formadmin=self,
            current_id=id)

    def create_view(self):
        self.return_url = request.args.get('next',
            url_for('.' + self.endpoint))

        obj = self.model()
        self.form = self.create_form(next=self.return_url, obj=obj)

        if self.form.validate_on_submit():
            if self.create_model(obj):
                if '_add_another' in request.form:
                    flash(_('Created successfully.'))
                    return redirect(url_for('.' + self.endpoint + '_create',
                        url=self.return_url))
                else:
                    return redirect(self.return_url)

        return render_template("create.html", formadmin=self)

    def edit_view(self, id):
        self.readonly = False
        self.return_url = request.args.get('next',
            url_for('.' + self.endpoint))

        obj = self.model.query.get(id)
        self.form = self.create_form(next=self.return_url, obj=obj)

        if self.form.validate_on_submit():
            if self.update_model(obj):
                return redirect(self.return_url)

        return render_template("edit.html", formadmin=self)

    def delete_view(self, id):
        self.return_url = request.args.get('next',
            url_for('.' + self.endpoint))

        obj = self.model.query.get(id)

        if obj:
            self.delete_model(obj)

        return redirect(self.return_url)
