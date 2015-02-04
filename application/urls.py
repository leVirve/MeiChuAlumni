"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

# Blessing messages list page
app.add_url_rule('/blessings', 'list_messages', view_func=views.list_messages, methods=['GET'])
app.add_url_rule('/blessings/more', 'more_message', view_func=views.more_messages, methods=['GET'])

# Blessing post message
app.add_url_rule('/blessings', 'new_message', view_func=views.new_message, methods=['GET', 'POST'])

# After leaving messages, visitor will receive a share button
app.add_url_rule('/blessings/update', view_func=views.update_message, methods=['GET', 'POST'])

# Contrived admin-only view
app.add_url_rule('/get/users/<int:uid>', 'get_users', view_func=views.get_users, methods=['GET', 'POST'])
app.add_url_rule('/get/raffle', 'admin_only', view_func=views.get_raffle_list, methods=['GET', 'POST'])


app.add_url_rule('/photo', 'photo_manage', view_func=views.photo_manage)

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

