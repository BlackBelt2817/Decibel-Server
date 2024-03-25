from flask import Flask, jsonify, request, Response, make_response, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import io
import json
import os
import sys
import threading
import time
from datetime import datetime

import picamera

from routes.camera_spare import routes_camera_spare, socket_init_camera_spare, cameraSpareStream, outputCameraSpareStream
from routes.chats import routes_chats, socket_init_chats
from routes.games import routes_games, socket_init_games
from routes.images import routes_images
from routes.languages import routes_languages
#from routes.misc import routes_misc
#from routes.playlists import routes_playlists
from routes.posts import routes_posts, socket_init_posts
#from routes.settings import routes_settings
from routes.songs import routes_songs
from routes.users import routes_users, socket_init_users
from routes.yt import routes_yt, socket_init_yt


curPath = os.path.dirname(__file__)
recordingsPath = curPath + '/recordings'

app = Flask(__name__)
CORS(app)

#@app.after_request
#def after_request(response: Response) -> Response:
#    response.access_control_allow_origin = '*'
#    return response

#CORS(app)
#app.config['SECRET_KEY'] = "APP_SECRET_KEY"
socketio = SocketIO(app, cors_allowed_origins='*')

app.register_blueprint(routes_camera_spare)
app.register_blueprint(routes_chats)
app.register_blueprint(routes_games)
app.register_blueprint(routes_images)
app.register_blueprint(routes_languages)
#app.register_blueprint(routes_misc)
#app.register_blueprint(routes_playlists)
app.register_blueprint(routes_posts)
#app.register_blueprint(routes_settings)
app.register_blueprint(routes_songs)
app.register_blueprint(routes_users)
app.register_blueprint(routes_yt)

socket_init_camera_spare(socketio)
socket_init_chats(socketio)
socket_init_games(socketio)
socket_init_posts(socketio)
socket_init_users(socketio)
socket_init_yt(socketio)

spare_camera_recording = False

cameraSpareStream.start_recording(outputCameraSpareStream, format='mjpeg', splitter_port=1)

@socketio.on('connect')
def test_connect():
    print('Client Connected')
#    print(data)
#    time.sleep(1)
#    if spare_camera_recording == False:
#        spare_camera_recording = True
#        cameraSpareStream.start_recording(outputCameraSpareStream, format='mjpeg', splitter_port=1)

@socketio.on('disconnect')
def test_disconnect():
    print('Client Disconnected')
#    print(data)
#    cameraSpareStream.stop_recording()
    
if __name__ == '__main__':
    socketio.run(app)