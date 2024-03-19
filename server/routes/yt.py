import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
import os
from pytube import YouTube

curPath = os.path.dirname(__file__)

musicPath = curPath + '/../../files/music'

routes_yt = Blueprint('routes_yt', __name__)