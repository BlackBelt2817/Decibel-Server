from flask import Flask, jsonify, request, Response, send_file
#from flask_socketio import SocketIO;
import sqlite3
import json
import os
import sys

from routes.images import routes_images
#from routes.playlists import routes_playlists
#from routes.settings import routes_settings
from routes.songs import routes_songs
from routes.users import routes_users

app = Flask(__name__)
#app.config['SECRET_KEY'] = "APP_SECRET_KEY"
#socketio = SocketIO(app)

app.register_blueprint(routes_images)
#app.register_blueprint(routes_playlists)
#app.register_blueprint(routes_settings)
app.register_blueprint(routes_songs)
app.register_blueprint(routes_users)

#    request_data = request.data
#    print(request_data)
#    request_args = request.args
#    print(request_args)
#    request_form = request.form
#    print(request_form)
#    request_files = request.files
#    print(request_files)
#    request_values = request.values
#    print(request_values)
#    request_json = request.json
#    print(request_json)
#    request_get_json = request.get_json()
#    print(request_get_json)
#    request_get_json_forced = request.get_json(force=True)
#    print(request_get_json_forced)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
#    socketio.run(app, debug=True)