# -*- coding: utf-8 -*-
"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from __future__ import division
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

from flask import request, render_template, flash, url_for, redirect, jsonify

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import MessageForm, departments
from models import MessageModel, User, CounterDB
from normalize import normalize

import json
import operator


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


@cache.cached(timeout=30)
def home():
    # may cause pjax error in QUERY ???!!
    messages = MessageModel.query().order(-MessageModel.timestamp).fetch(5)
    counts, counter = get_heading_department()
    return pjax('main_page.html',
                messages=messages,
                counts=counts,
                counter=counter)


def list_messages():
    return pjax('blessings.html',
                messageset=get_heading_depart_messages(),
                form=MessageForm())


def more_messages():
    form = MessageForm()
    department = form.department.data
    grade = form.grade.data
    messages = MessageModel.query(ndb.AND(MessageModel.department==department, MessageModel.grade==grade)).order(-MessageModel.timestamp).fetch(30)
    return pjax('messages.html',
                messages=messages,
                form=MessageForm(),
                query=1)


def new_message():
    """ New message into database """
    form = MessageForm()
    if form.validate_on_submit():
        try:
            message = MessageModel(
                    name=form.name.data,
                    department=form.department.data,
                    grade=form.grade.data,
                    phone=form.phone.data,
                    mail=form.mail.data,
                    description=form.description.data,
                    )
            query = User.query(User.phone == form.phone.data)
            if not query.get():
                user = User(
                    name=form.name.data,
                    department=form.department.data,
                    grade=form.grade.data,
                    phone=form.phone.data,
                    mail=form.mail.data,
                    account=form.account.data
                    )
                key_string = u'%s%s' % (form.department.data, form.grade.data)
                counter = CounterDB.get_by_id(key_string)
                if counter is None:
                    counter = CounterDB(id=key_string)
                counter.val += 1
                counter.put()
                user.put()
            message.put()
            message_id = message.key.id()
            return jsonify(mid=message_id)
        except ValueError:
            return redirect(url_for('list_messages'))
    return jsonify(error='Please refill the form'), 400


def update_message():
    if request.method == "POST":
        message_id = int(request.form.get('d'))
        message = MessageModel.get_by_id(message_id)
        user = User.query(User.phone == message.phone).get()
        if message and request.form.get('c'):
            message.shared = True
            user.shared = True
            message.put()
            user.put()
            return redirect(url_for('list_messages'), 302)
        return redirect(url_for('list_messages'), 400)


def photo():
    return pjax('photo.html')


def content():
    return pjax('content.html')


def morepage():
    form = MessageForm()
    return pjax('messages.html', form=form)


@cache.cached(timeout=600) #, key_prefix='depart_counts')
def get_heading_department(num=10):
    counts = CounterDB.query()
    result, counter = [], 0
    for c in counts:
        key, val = u'%s' % c.key.id().decode('utf8'), c.val
        counter += val
        if key in normalize:
            val = val * 100 / normalize[key]
            if val > 0: result.append((val, key))
    result = sorted(result, key=operator.itemgetter(0), reverse=True)
    return result[:10], counter
    

@cache.cached(timeout=600) #, key_prefix='depart_comments')
def get_heading_depart_messages():
    messageset = {} 
    departs = MessageModel.query(projection=["department", "description"])
    for m in departs:
        d = m.department
        messageset[d] = MessageModel.query(MessageModel.department == d).fetch(10)
    return messageset


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'admin_page'


def get_heading_department_none_cached(num):
    counts = CounterDB.query()
    result = []
    for c in counts:
        key, val = u'%s' % c.key.id().decode('utf8'), c.val
        if key in normalize:
            val = val * 100 / normalize[key]
            if val > 0: result.append((val, key))
    result = sorted(result, key=operator.itemgetter(0), reverse=True)
    return result[:num]


@admin_required
def get_users(uid):
    if uid:
        user = User.get_by_id(uid)
        return jsonify(user=user.to_dict())


@admin_required
def get_raffle_list():
    """ Get the list of user id and shared state for raffle """
    if request.method == "POST":
        candidates = get_heading_department_none_cached(3)
        result = {}
        app.logger.debug(candidates)
        for candidate in candidates:
            department, grade = candidate[1][:-2], candidate[1][-2:]
            users = User.query(ndb.AND(User.department==department, User.grade==grade))
            data = [{'shared': p.shared, 'id': p.key.id() } for p in users]
            result[candidate] = data
            app.log.debug(data)
        return jsonify(rafflelist=result)
    return render_template('admin.html')


def pjax(template, **kwargs):
    """Test whether the request was with PJAX or not."""
    if "X-PJAX" in request.headers:
        return render_template(template, **kwargs)
    return render_template("base.html", template=template, **kwargs)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
