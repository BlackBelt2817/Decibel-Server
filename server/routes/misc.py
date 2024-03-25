import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
import json
from flask_socketio import emit

routes_misc = Blueprint('routes_misc', __name__)

@routes_misc.route('/misc/sql/post', methods=['POST'])
def insertMiscData():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        k = requestData['key']
        v = requestData['value']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO misc VALUES (?, ?)", (k, v))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': e})

