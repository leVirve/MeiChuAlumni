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
from forms import MessageForm, departments
from models import MessageModel, User
import fastcounter

import json
import operator

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


#@cache.cached(timeout=200)
def home():
    MsgQuery = MessageModel.query().order(-MessageModel.timestamp)
    messages, next_curs, more = MsgQuery.fetch_page(6, start_cursor=Cursor())
    next_curs = next_curs.urlsafe() if more else None
    return pjax('main_page.html',
                messages=messages,
                next_curs=next_curs, more=more,
                counts=get_heading_department())


#@cache.cached(timeout=60)
def list_messages():
    counts = get_heading_department()
    messageset = {}
    for department, val in counts:
        messageset[department] = MessageModel.query(MessageModel.department==department).order(-MessageModel.timestamp).fetch(10)
    # MsgQuery = MessageModel.query().order(-MessageModel.timestamp)
    # curs = Cursor(urlsafe=request.args.get('cursor'))
    # messages, next_curs, more = MsgQuery.fetch_page(20, start_cursor=curs)
    # next_curs = next_curs.urlsafe() if more else None
    form = MessageForm()
    return pjax('blessings.html',
                messageset=messageset, form=form,
                # next_curs=next_curs, more=more,
                # counts=counts
                )


def more_messages(department=None):
    MsgQuery = MessageModel.query().order(-MessageModel.timestamp)
    curs = Cursor(urlsafe=request.args.get('cursor'))
    messages, next_curs, more = MsgQuery.fetch_page(20, start_cursor=curs)
    data = [dict(p.to_dict(include=[
            'grade','department','timestamp','description'])
            ) for p in messages]
    return jsonify(messages=data, next_src=next_curs.urlsafe(), more=more)


def new_message():
    """ New message into database """
    form = MessageForm()
    if form.validate_on_submit():
        try:
            message = MessageModel(
                    name=form.name.data,
                    department=form.department.data,
                    grade=int(form.grade.data),
                    phone=form.phone.data,
                    mail=form.mail.data,
                    description=form.description.data,
                    )
            query = User.query(User.phone == form.phone.data)
            if not query.get():
                user = User(
                    name=form.name.data,
                    department=form.department.data,
                    grade=int(form.grade.data),
                    phone=form.phone.data,
                    mail=form.mail.data,
                    )
                user.put()
            message.put()
            message_id = message.key.id()
            fastcounter.incr(form.department.data)
            return jsonify(mid=message_id)
        except ValueError:
            return redirect(url_for('list_messages'))


def update_message():
    if request.method == "POST":
        message_id = int(request.form.get('d'))
        message_future = MessageModel.get_by_id(message_id)
        user = User.query(User.phone == message.phone).get()
        message = message_future.get_result()
        if message and request.form.get('c'):
            message.shared = True
            user.shared = True
            message.put()
            user.put()
            return redirect(url_for('list_messages'), 302)


def photo():
    return pjax('photo.html')


def content():
    return pjax('content.html')


@cache.cached(timeout=600, key_prefix='depart_counts')
def get_heading_department(num=10):
    counts = [v for v in fastcounter.get_counts(departments)]
    d = dict(zip(departments, counts))
    d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    return d[:num]


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'admin_page'


@admin_required
def get_users(uid):
    if uid:
        user = User.get_by_id(uid)
        return jsonify(user=user.to_dict())


@admin_required
def get_raffle_list():
    """ Get the list of user id and shared state for raffle """
    if request.method == "POST":
        import datetime
        period = datetime.datetime.now() - datetime.timedelta(weeks=1)
        users = User.query().filter(User.timestamp >= period)
        data = [{'shared': p.shared, 'id': p.key.id() } for p in users]
        return jsonify(rafflelist=data)
    return render_template('admin.html')


def pjax(template, **kwargs):
    """Test whether the request was with PJAX or not."""
    if "X-PJAX" in request.headers:
        app.logger.debug('pjax')
        return render_template(template, **kwargs)
    return render_template("base.html", template=template, **kwargs)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
