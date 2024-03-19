import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
import json
from flask_socketio import emit

routes_chats = Blueprint('routes_chats', __name__)

@routes_chats.route('/chats/sql/addUsersToChat', methods=['POST'])
def addUsersToChat():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        userIdsFromClient = requestData['userIds']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT user_ids from chats WHERE _ID = ?", (chatId,))
        
        oldUserIds = cursor.fetchone()[0]
        updatedUserIds = json.loads(oldUserIds)
        
        for userId in userIdsFromClient:
            updatedUserIds.append(userId)

        cursor.execute("UPDATE chats SET user_ids = ? WHERE _ID = ?", (json.dumps(updatedUserIds), chatId,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': userIdsFromClient, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_chats.route('/chats/sql/create', methods=['POST'])
def createChat():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        userIds = json.dumps(requestData['userIds'])
        messages = json.dumps(requestData['messages'])
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO chats VALUES (?, ?, ?)", (None, userIds, messages,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_chats.route('/chats/sql/get/byUserId', methods=['POST'])
def getChatsByUserId():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        userId = requestData['userId']
#        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM chats WHERE user_ids LIKE ?", ('%' + str(userId) + '%',))
        chats = cursor.fetchall()
        finalChats = []
        sqliteConnection.commit()
        sqliteConnection.close()
        
        if len(chats) < 1:
            return jsonify({'data': [], 'success': True})
        else:
            for chat in chats:
                currentChat = {
                    '_ID': chat[0],
                    'user_ids': json.loads(chat[1]),
                    'messages': json.loads(chat[2])
                }
                finalChats.append(currentChat)
            return jsonify({'data': finalChats, 'success': True})
    
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_chats.route('/chats/sql/sendMessage', methods=['POST'])
def sendMessage():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        message = requestData['message']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT messages from chats WHERE _ID = ?", (chatId,))
        
        oldMessages = cursor.fetchone()[0]
        updatedMessages = json.loads(oldMessages)
        updatedMessages.append(message)

        cursor.execute("UPDATE chats SET messages = ? WHERE _ID = ?", (json.dumps(updatedMessages), chatId,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': message, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    




def socket_init_chats(socketio):
    
    @socketio.on('addUsersToChat')
    def addUsersToChat(data):
        emit('addUsersToChat', data, broadcast=True)
    
    @socketio.on('createChat')
    def createChat(data):
        creator = data['creator']
        chatOptions = data['chatOptions']
        userIds = json.dumps(chatOptions['userIds'])
        timeStamp = chatOptions['messages'][0]['timeStamp']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM chats WHERE user_ids = ? AND messages LIKE ?", (userIds, '%' + timeStamp + '%',))
        chat = cursor.fetchone()
        finalChat = {
            '_ID': chat[0],
            'userIds': json.loads(chat[1]),
            'messages': json.loads(chat[2])
        }
        sqliteConnection.commit()
        sqliteConnection.close()
        
        emit('createChat', {'creator': creator, 'chatOptions': finalChat}, broadcast=True)
        
    @socketio.on('sendMessage')
    def sendMessage(data):
        emit('sendMessage', data, broadcast=True)
        
        















