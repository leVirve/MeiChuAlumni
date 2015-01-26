"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class MessageModel(ndb.Model):
    """Message Model"""
    name        = ndb.StringProperty(required=True)
    school      = ndb.StringProperty(required=True)
    department  = ndb.StringProperty(required=True)
    phone       = ndb.IntegerProperty(required=True)
    mail        = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    shared      = ndb.BooleanProperty(default=False)
    timestamp   = ndb.DateTimeProperty(auto_now_add=True)
