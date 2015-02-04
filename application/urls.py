"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views
from application import fastcounter


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Main
app.add_url_rule('/', view_func=views.home)
app.add_url_rule('/index', view_func=views.home)
app.add_url_rule('/content', view_func=views.content)
app.add_url_rule('/photo', view_func=views.photo)
app.add_url_rule('/blessings', view_func=views.list_messages)
app.add_url_rule('/more', view_func=views.morepage)
app.add_url_rule('/more', 'more_message', view_func=views.more_messages, methods=['POST'])
app.add_url_rule('/blessings', 'new_message', view_func=views.new_message, methods=['POST'])
app.add_url_rule('/blessings/update', view_func=views.update_message, methods=['POST'])


# Contrived admin-only view
app.add_url_rule('/get/users/<int:uid>', 'get_users', view_func=views.get_users, methods=['GET', 'POST'])
app.add_url_rule('/get/raffle', 'admin_only', view_func=views.get_raffle_list, methods=['GET', 'POST'])


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
