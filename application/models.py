"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class MessageModel(ndb.Model):
    """Message Model"""
    name        = ndb.StringProperty(required=True)
    department  = ndb.StringProperty(required=True)
    grade       = ndb.StringProperty(required=True)
    phone       = ndb.StringProperty(required=True)
    mail        = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    shared      = ndb.BooleanProperty(default=False)
    timestamp   = ndb.DateTimeProperty(auto_now_add=True)


class User(ndb.Model):
    """ User Model """
    name        = ndb.StringProperty(required=True)
    department  = ndb.StringProperty(required=True)
    grade       = ndb.StringProperty(required=True)
    phone       = ndb.StringProperty(required=True)
    mail        = ndb.StringProperty(required=True)
    account     = ndb.StringProperty()
    shared      = ndb.BooleanProperty(default=False)
    timestamp   = ndb.DateTimeProperty(auto_now=True)


class CounterDB(ndb.Model):
    """ Counter in db Model """
    val         = ndb.IntegerProperty(default=0)
