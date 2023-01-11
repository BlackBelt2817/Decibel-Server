import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
import json

routes_users = Blueprint('routes_users', __name__)

@routes_users.route('/users/sql/byEmail', methods=['POST'])
def getUserByEmail():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        email = requestData['email']
        finalUser = None
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user != None:
            finalUser = {
                '_ID': user[0],
                'email': user[1],
                'username': user[2],
                'password': user[3],
                'admin': user[4]
            }
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalUser, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_users.route('/users/sql/byUsername', methods=['POST'])
def getUserByUsername():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        username = requestData['username']
        finalUser = None
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user != None:
            finalUser = {
                '_ID': user[0],
                'email': user[1],
                'username': user[2],
                'password': user[3],
                'admin': user[4]
            }
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalUser, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_users.route('/users/sql/register', methods=['POST'])
def registerUser():
    try:
        requestForm = request.form
        requestData = requestForm['data']
        email = requestData['email']
        username = requestData['username']
        password = requestData['password']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (None, email, username, password, 0))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestForm, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

