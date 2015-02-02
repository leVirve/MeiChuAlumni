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
from google.appengine.datastore.datastore_query import Cursor

from flask import request, render_template, flash, url_for, redirect, jsonify

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import MessageForm
from models import MessageModel, User
import counter
import json

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def home():
    return redirect(url_for('list_messages'))


def list_messages():
    """List all massages"""
    MsgQuery = MessageModel.query().order(-MessageModel.timestamp)
    curs = Cursor(urlsafe=request.args.get('cursor'))
    messages, next_curs, more = MsgQuery.fetch_page(3, start_cursor=curs)
    if not curs.urlsafe():
        form = MessageForm()
        nthu, nctu = counter.get_count(u'清華大學'), counter.get_count(u'交通大學')
        next_curs = next_curs.urlsafe() if more else None
        return render_template('base.html',
                    messages=messages,
                    form=form,
                    next_curs=next_curs, more=more,
                    nthu=nthu, nctu=nctu)
    data = ([dict(p.to_dict(
                include=['school', 'department', 'timestamp', 'description']))
                for p in messages])
    return jsonify(messages=data, next_src=next_curs.urlsafe(), more=more)


def new_message():
    """ New message into database """
    form = MessageForm()
    if form.validate_on_submit():
        try:
            message = MessageModel(
                    name=form.name.data,
                    school=form.school.data,
                    department=form.department.data,
                    phone=form.phone.data,
                    mail=form.mail.data,
                    description=form.description.data,
                    )
            user = User(
                    name=form.name.data,
                    school=form.school.data,
                    department=form.department.data,
                    phone=form.phone.data,
                    mail=form.mail.data,
                    )
            query = User.query(User.phone == user.phone)

            if not query.count():
                user.put()
            message.put()
            message_id = message.key.id()
            counter.increment(form.school.data)
            return jsonify(mid=message_id)
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_messages'))
        except ValueError:
            return redirect(url_for('list_messages'))


def update_message():
    if request.method == "POST":
        message_id = int(request.form.get('d'))
        message = MessageModel.get_by_id(message_id)
        user    = User.query(User.phone == message.phone).get()
        if message and request.form.get('c'):
            message.shared = True
            user.shared = True
            message.put()
            user.put()
            flash(u'Share success', 'success')
            return redirect(url_for('list_messages'), 302)


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
    import datetime
    period = datetime.datetime.now() - datetime.timedelta(weeks=1)    
    users = User.query().filter(User.timestamp >= period)
    return render_template('admin.html', users=users) 


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

