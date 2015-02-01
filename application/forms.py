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


class ClassicMessageForm(wtf.Form):
    name        = wtf.StringField(u'姓名', validators=[validators.Required()])
    school      = wtf.RadioField(u'學校', choices=[('NTHU', u'清華大學'), ('NCTU', u'交通大學')],validators=[validators.Required()])
    department  = wtf.StringField(u'系級', validators=[validators.Required()])
    phone       = wtf.StringField(u'聯絡電話', validators=[validators.Required()])
    mail        = wtf.StringField(u'聯絡信箱', validators=[validators.Required()])
    description = wtf.TextAreaField(u'祝福', validators=[validators.Required()])


MessageForm = model_form(MessageModel, ClassicMessageForm, field_args={
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
        'validators': [validators.Required(), validators.AnyOf([(u'清華大學'), (u'交通大學')])]
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
        'validators': [validators.Required(), validators.Email()]
    },
    'description': {
        'label': u'祝福的話',
        'description': u'blessing',
        'validators': [validators.Required()]
    },
})

