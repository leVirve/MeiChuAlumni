# -*- coding: utf-8 -*-
"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""
from flaskext import wtf
from flaskext.wtf import validators, recaptcha
from wtforms.ext.appengine.ndb import model_form
from flaskext.wtf.recaptcha.fields import RecaptchaField

from .models import MessageModel
import secret_keys

departments = [
u"人人文社會學系人社院學士班",
u"工程與系統科學系",
u"工業工程與工程管理學系",
u"工業工程與工程管理學系工工組",
u"工業工程與工程管理學系工管組",
u"工業工程與工程管理學系在職專班",
u"工學院學士班",
u"中國文學系",
u"中國文學系文學所",
u"分子生物研究所",
u"分子與細胞生物研究所",
u"分子醫學研究所",
u"化學工程學系",
u"化學系理學院學士班",
u"半導體元件及製程產研發碩士專班",
u"台灣文學研究所",
u"台灣研究教師在職進修碩士學位",
u"外國語文學系",
u"外國語言學系",
u"生命科學系",
u"生命科學院學士班",
u"生物技術研究所",
u"生物科技研究所",
u"生物資訊與結構生物研究所",
u"生物醫學工程研究所",
u"生物醫學研究所",
u"生醫工程與環境科學系",
u"先進光源科技碩士學位學程工科組",
u"先進光源科技碩士學位學程物理組",
u"光電工程研究所",
u"光電科技產業研發碩士專班",
u"材料科學工程學系",
u"系統神經科學研究所",
u"奈米工程與微系統研究所",
u"服務科學研究所碩士班",
u"物理系不分組",
u"物理系光電物理組",
u"物理系物理組",
u"物理系應用物理組",
u"社會人類學研究所",
u"社會學研究所",
u"科技法律研究所",
u"科技管理研究所",
u"科技管理學院學士班",
u"計量財務金融學系",
u"原子科學院學士班",
u"哲學研究所",
u"高分子研究所",
u"高階主管經營管理EMBA",
u"動力機械工程學系",
u"國際專業管理碩士IMBA",
u"統計學研究所",
u"通訊工程研究所",
u"經濟學系",
u"經營管理碩士在職專班",
u"資訊工程學系",
u"資訊工程學系計管所",
u"資訊系統與應用研究所",
u"電力電子產業研發碩士專班",
u"電子工程研究所",
u"電機工程學系",
u"電機資訊學院學士班",
u"語言學研究所",
u"數學系不分組",
u"數學系純粹數學組",
u"數學系應用數學組",
u"學習科學研究所",
u"歷史研究所",
u"積體電路產業研發碩士專班",
u"醫學科學系",
]

class ClassicMessageForm(wtf.Form):
    name        = wtf.StringField(u'姓名', validators=[validators.Required()])
    department  = wtf.SelectField(u'系級', choices=departments, validators=[validators.Required()])
    grade       = wtf.StringField(u'系級', validators=[validators.Required()])
    phone       = wtf.StringField(u'聯絡電話', validators=[validators.Required()])
    mail        = wtf.StringField(u'聯絡信箱', validators=[validators.Required()])
    account     = wtf.StringField(u'聯絡')
    description = wtf.TextAreaField(u'祝福', validators=[validators.Required()])
    recaptcha   = RecaptchaField()


MessageForm = model_form(MessageModel, ClassicMessageForm, field_args={
    'name': {
        'label': u'姓名',
        'description': 'Your name',
        'validators': [validators.Required()]
        },
    'grade': {
        'label': u'系級',
        'description': u'Number',
        'validators': [validators.Required()]
        },
    'department': {
        'label': u'系級',
        'choices': departments,
        'description': u'例如: 資工系',
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
    'account': {
        'label': u'聯絡'
        },
    'description': {
        'label': u'祝福的話',
        'description': u'blessing',
        'validators': [validators.Required()]
        },
    })

