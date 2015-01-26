# -*- coding: utf-8 -*-
"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import MessageForm
from models import MessageModel


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def home():
    return redirect(url_for('list_messages'))


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username


# @login_required
def list_messages():
    """List all massages"""
    messages = MessageModel.query()
    form = MessageForm()
    if form.validate_on_submit():
        message = MessageModel(
            name=form.name.data,
            school=form.school.data,
            department=form.department.data,
            phone=form.phone.data,
            mail=form.mail.data,
            #shared
            description=form.description.data,
        )
        """ Check for duplicate  """
        query = MessageModel.query(MessageModel.phone==message.phone)
        if query:
            flash(u'你已經填過囉！', 'info')
            return redirect(url_for('list_messages'), 302)
        try:
            message.put()
            message_id = message.key.id()
            flash(u'Message %s successfully saved.' % message_id, 'success')
            return redirect(url_for('list_messages'), 302)
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_messages'))
    return render_template('list_messages.html', messages=messages, form=form)


@login_required
def edit_message(message_id):
    message = MessageModel.get_by_id(message_id)
    form = MessageForm(obj=message)
    if request.method == "POST":
        if form.validate_on_submit():
            # example.example_name = form.data.get('example_name')
            # example.example_description = form.data.get('example_description')
            # example.put()
            flash(u'Message %s successfully saved.(Test Not Really)' % message_id, 'success')
            return redirect(url_for('list_messages'))
    return render_template('edit_message.html', message=message, form=form)


@login_required
def delete_message(message_id):
    """Delete an message object"""
    message = MessageModel.get_by_id(message_id)
    if request.method == "POST":
        try:
            message.key.delete()
            flash(u'Message %s successfully deleted.' % message_id, 'success')
            return redirect(url_for('list_messages'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_messages'))


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


@cache.cached(timeout=60)
def cached_messages():
    """This view should be cached for 60 sec"""
    messages = MessageModel.query()
    return render_template('list_messages_cached.html', messages=messages)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

