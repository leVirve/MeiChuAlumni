# -*- coding: utf-8 -*-
"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""
from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import MessageModel


MessageForm = model_form(MessageModel, wtf.Form, field_args={
# App Engine ndb model form
    'name': {
        'label': u'姓名',
        'description': 'Your name',
        'validators': [validators.Required()]
    },
    'school': {
        'label': u'學校',
        'description': u'NTHU / NCTU',
	'choices': [(u'清華大學'), (u'交通大學')],
        'validators': [validators.Required()]
    },
    'department': {
        'label': u'系級',
        'description': u'例如: 資工系 16',
        'validators': [validators.Required()]
    },
    'phone': {
        'label': u'連絡電話',
        'description': u'聯絡必要資料',
        'validators': [validators.Required()]
    },
    'mail': {
        'label': u'聯絡信箱',
        'description': u'聯絡必要資料',
        'validators': [validators.Required()]
    },
    'description': {
        'label': u'祝福的話',
        'description': u'blessing',
        'validators': [validators.Required()]
    },
})
