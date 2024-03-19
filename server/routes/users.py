import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
from flask_socketio import emit
import json

routes_users = Blueprint('routes_users', __name__)

@routes_users.route('/users/sql/get/allChatUsersByUserId', methods=['POST'])
def getAllChatUsersByUserId():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        userId = requestData['userId']

        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
#        sqlExecStatementForAllUserChats = 
        cursor.execute("SELECT * FROM chats WHERE user_ids = ? OR user_ids LIKE ? OR user_ids LIKE ? OR user_ids LIKE ?", ('[' + str(userId) + ']', '%, ' + str(userId) + ',%', '[' + str(userId) + ', %', '%, ' + str(userId) + ']'))
        userChats = cursor.fetchall()
        allUserIds = []
        
        if len(userChats) < 1:
            return jsonify({'data': [], 'success': True})
        else:
            for userChat in userChats:
                innerUserIds = json.loads(userChat[1])
                for innerUserId in innerUserIds:
                    if innerUserId not in allUserIds:
                        allUserIds.append(innerUserId)
                        
        sqlExecStatement = "SELECT * FROM users WHERE _ID IN ({seq})".format(seq=','.join(['?']*len(allUserIds)))
        cursor.execute(sqlExecStatement, allUserIds)
        users = cursor.fetchall()
                
        sqliteConnection.commit()
        sqliteConnection.close()
        
        allUsers = []
        
        for user in users:
            currentUser = {
                '_ID': user[0],
                'email': user[1],
                'username': user[2],
                'admin': user[4],
                'firstName': user[5],
                'lastName': user[6],
#                    'birthYear': friend[7],
#                    'birthMonth': friend[8],
#                    'birthDay': friend[9],
                'friendRequestsOutgoing': json.loads(user[7]),
                'friendRequestsIncoming': json.loads(user[8]),
                'friends': json.loads(user[9])
            }
            allUsers.append(currentUser)
        return jsonify({'data': allUsers, 'success': True})
        
#        if len(friends) < 1:
#            return jsonify({'data': [], 'success': True})
#        else:
#            for friend in friends:
#                currentFriend = {
#                    '_ID': friend[0],
#                    'email': friend[1],
#                    'username': friend[2],
#                    'password': friend[3],
#                    'admin': friend[4],
#                    'firstName': friend[5],
#                    'lastName': friend[6],
##                    'birthYear': friend[7],
##                    'birthMonth': friend[8],
##                    'birthDay': friend[9],
#                    'friendRequestsOutgoing': json.loads(friend[7]),
#                    'friendRequestsIncoming': json.loads(friend[8]),
#                    'friends': json.loads(friend[9])
#                    
#                }
#                finalFriends.append(currentFriend)
#            return jsonify({'data': finalFriends, 'success': True})
        return jsonify({'data': finalUsers, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_users.route('/users/sql/get/friendsBySearchTerm', methods=['POST'])
def getFriendsBySearchTerm():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        searchTerm = requestData['searchTerm']
        userId = requestData['userId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT u.*, u.first_name || ' ' || u.last_name AS full_name FROM users u WHERE (friends = ? OR friends LIKE ? OR friends LIKE ? OR friends LIKE ?) AND (email LIKE ? OR username LIKE ? OR first_name LIKE ? OR last_name LIKE ? OR full_name LIKE ?) ORDER BY first_name, last_name", ('[' + str(userId) + ']', '%,' + str(userId) + ',%', '[' + str(userId) + ',%', '%,' + str(userId) + ']', '%' + searchTerm + '%', '%' + searchTerm + '%', '%' + searchTerm + '%', '%' + searchTerm + '%', '%' + searchTerm + '%',))
        friends = cursor.fetchall()
        finalFriends = []
        sqliteConnection.commit()
        sqliteConnection.close()
        
        if len(friends) < 1:
            return jsonify({'data': [], 'success': True})
        else:
            for friend in friends:
                currentFriend = {
                    '_ID': friend[0],
                    'email': friend[1],
                    'username': friend[2],
                    'admin': friend[4],
                    'firstName': friend[5],
                    'lastName': friend[6],
                    'friendRequestsOutgoing': json.loads(friend[7]),
                    'friendRequestsIncoming': json.loads(friend[8]),
                    'friends': json.loads(friend[9])
                }
                finalFriends.append(currentFriend)
            return jsonify({'data': finalFriends, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_users.route('/users/sql/get/friendsByUserId', methods=['POST'])
def getFriendsByUserId():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        userId = requestData['userId']

        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM users WHERE friends LIKE ? ORDER BY first_name, last_name", ('%' + str(userId) + '%',))
        friends = cursor.fetchall()
        finalFriends = []
        sqliteConnection.commit()
        sqliteConnection.close()
        
        if len(friends) < 1:
            return jsonify({'data': [], 'success': True})
        else:
            for friend in friends:
                currentFriend = {
                    '_ID': friend[0],
                    'email': friend[1],
                    'username': friend[2],
                    'password': friend[3],
                    'admin': friend[4],
                    'firstName': friend[5],
                    'lastName': friend[6],
#                    'birthYear': friend[7],
#                    'birthMonth': friend[8],
#                    'birthDay': friend[9],
                    'friendRequestsOutgoing': json.loads(friend[7]),
                    'friendRequestsIncoming': json.loads(friend[8]),
                    'friends': json.loads(friend[9])
                    
                }
                finalFriends.append(currentFriend)
            return jsonify({'data': finalFriends, 'success': True})
        return jsonify({'data': finalUsers, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_users.route('/users/sql/get/byUserId', methods=['POST'])
def getUserByUserId():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        userId = requestData['userId']

        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM users WHERE _ID = ?", (userId,))
        friend = cursor.fetchone()
        sqliteConnection.commit()
        sqliteConnection.close()
        
        if friend == None:
            return jsonify({'data': None, 'success': True})
        else:
            finalFriend = {
                '_ID': friend[0],
                'email': friend[1],
                'username': friend[2],
                'password': friend[3],
                'admin': friend[4],
                'firstName': friend[5],
                'lastName': friend[6],
#                    'birthYear': friend[7],
#                    'birthMonth': friend[8],
#                    'birthDay': friend[9],
                'friendRequestsOutgoing': json.loads(friend[7]),
                'friendRequestsIncoming': json.loads(friend[8]),
                'friends': json.loads(friend[9])
            }
            return jsonify({'data': finalFriend, 'success': True})
        return jsonify({'data': finalUsers, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_users.route('/users/sql/get/byUserIdList', methods=['POST'])
def getUsersByUserIdList():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        userIdList = requestData['userIdList']

        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
#        cursor.execute("SELECT * FROM users WHERE _ID IN (?)", (','.join(map(str, userIdList)),))
        sqlExecStatement = "SELECT * FROM users WHERE _ID IN ({seq})".format(seq=','.join(['?']*len(userIdList)))
        cursor.execute(sqlExecStatement, userIdList)
        users = cursor.fetchall()
        sqliteConnection.commit()
        sqliteConnection.close()
        allUsers = []
        
        for user in users:
            currentUser = {
                '_ID': user[0],
                'email': user[1],
                'username': user[2],
                'password': user[3],
                'admin': user[4],
                'firstName': user[5],
                'lastName': user[6],
#                    'birthYear': friend[7],
#                    'birthMonth': friend[8],
#                    'birthDay': friend[9],
                'friendRequestsOutgoing': json.loads(user[7]),
                'friendRequestsIncoming': json.loads(user[8]),
                'friends': json.loads(user[9])
            }
            allUsers.append(currentUser)
        return jsonify({'data': allUsers, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})










@routes_users.route('/users/sql/bySearchTerm', methods=['POST'])
def getUsersBySearchTerm():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        searchTerm = requestData['searchTerm']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT u.*, u.first_name || ' ' || u.last_name AS full_name FROM users u WHERE email LIKE ? OR username LIKE ? OR first_name LIKE ? OR last_name LIKE ? OR full_name LIKE ? ORDER BY first_name, last_name", ('%' + searchTerm + '%', '%' + searchTerm + '%', '%' + searchTerm + '%', '%' + searchTerm + '%', '%' + searchTerm + '%',))
        users = cursor.fetchall()
        finalUsers = []
        
        for row in users:
            currentUser = {
                '_ID': row[0],
                'email': row[1],
                'username': row[2],
                'admin': row[4],
                'first_name': row[5],
                'last_name': row[6],
                'friend_requests_outgoing': json.loads(row[7]),
                'friend_requests_incoming': json.loads(row[8]),
                'friends': json.loads(row[9])
            }
            finalUsers.append(currentUser)
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalUsers, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

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
                'admin': user[4],
                'firstName': user[5],
                'lastName': user[6],
                'friend_requests_outgoing': json.loads(user[7]),
                'friend_requests_incoming': json.loads(user[8]),
                'friends': json.loads(user[9])
            }
        sqliteConnection.commit()
        sqliteConnection.close()
        
#        res = jsonify({'data': finalUser, 'success': True})
#        res.headers.add('Access-Control-Allow-Origin', '*')
#        return res
        
        return jsonify({'data': finalUser, 'success': True})
    except Exception as e:
#        res = jsonify({'data': None, 'success': False, 'error': e})
#        res.headers.add('Access-Control-Allow-Origin', '*')
#        return res
    
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
                'admin': user[4],
                'firstName': user[5],
                'lastName': user[6],
                'friend_requests_outgoing': json.loads(user[7]),
                'friend_requests_incoming': json.loads(user[8]),
                'friends': json.loads(user[9])
            }
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalUser, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_users.route('/users/sql/register', methods=['POST'])
def registerUser():
    try:
#        requestForm = request.form
#        requestData = requestForm['data']
        requestJson = request.get_json()
        requestData = requestJson['data']
        email = requestData['email']
        username = requestData['username']
        password = requestData['password']
        firstName = requestData['firstName']
        lastName = requestData['lastName']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, email, username, password, 0, firstName, lastName, '[]', '[]', '[]'))
        userId = cursor.lastrowid
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': {**requestData, 'userId': userId}, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_users.route('/users/sql/friendRequest', methods=['POST'])
def updateFriendRequest():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        myId = requestData['myId']
        myIncomingRequests = requestData['myIncomingRequests']
        myOutgoingRequests = requestData['myOutgoingRequests']
        myFriends = requestData['myFriends']
        theirId = requestData['theirId']
        theirIncomingRequests = requestData['theirIncomingRequests']
        theirOutgoingRequests = requestData['theirOutgoingRequests']
        theirFriends = requestData['theirFriends']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE users SET friend_requests_outgoing = ?, friend_requests_incoming = ?, friends = ? WHERE _ID = ?", (json.dumps(myOutgoingRequests), json.dumps(myIncomingRequests), json.dumps(myFriends), myId,))
        cursor.execute("UPDATE users SET friend_requests_outgoing = ?, friend_requests_incoming = ?, friends = ? WHERE _ID = ?", (json.dumps(theirOutgoingRequests), json.dumps(theirIncomingRequests), json.dumps(theirFriends), json.dumps(theirId),))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
    
    
    
    
    
    
    
    
    
def socket_init_users(socketio):
    @socketio.on('updateSentFriendRequest')
    def updateSentFriendRequest(data):
        action = data['action']
        myUserId = data['myUserId']
        theirUserId = data['theirUserId']
        friendRequestData = {
            'myUserId': myUserId,
            'theirUserId': theirUserId
        }
        if action == 'send':
            emit('sendFriendRequest', friendRequestData, broadcast=True)
        elif action == 'cancel':
            emit('cancelFriendRequest', friendRequestData, broadcast=True)
            
    @socketio.on('updateReceivedFriendRequest')
    def updateReceivedFriendRequest(data):
        action = data['action']
        myUserId = data['myUserId']
        theirUserId = data['theirUserId']
        friendRequestData = {
            'myUserId': myUserId,
            'theirUserId': theirUserId
        }
        if action == 'accept':
            emit('acceptFriendRequest', friendRequestData, broadcast=True)
        elif action == 'deny':
            emit('denyFriendRequest', friendRequestData, broadcast=True)

