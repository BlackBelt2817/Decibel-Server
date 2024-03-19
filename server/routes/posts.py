import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
import json
from flask_socketio import emit

routes_posts = Blueprint('routes_posts', __name__)

@routes_posts.route('/posts/sql/addCommentToComment', methods=['POST'])
def addCommentToComment():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        commentId = None
        parentId = requestData['parent_id']
        postId = requestData['post_id']
        authorId = requestData['author_id']
        content = requestData['content']
        likes = '[]'
        dislikes = '[]'
        taggedFriendIds = json.dumps(requestData['tagged_friend_ids'])
        timeStamp = requestData['time_stamp']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (commentId, parentId, postId, authorId, content, likes, dislikes, taggedFriendIds, timeStamp))
        commentId = cursor.lastrowid
        
        newComment = {
            '_ID': commentId,
            'parent_id': parentId,
            'post_id': postId,
            'author_id': authorId,
            'content': content,
            'likes': json.loads(likes),
            'dislikes': json.loads(dislikes),
            'tagged_friend_ids': json.loads(taggedFriendIds),
            'time_stamp': timeStamp
        }

        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': newComment, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_posts.route('/posts/sql/addCommentToPost', methods=['POST'])
def addCommentToPost():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        commentId = None
        parentId = None
        postId = requestData['post_id']
        authorId = requestData['author_id']
        content = requestData['content']
        likes = '[]'
        dislikes = '[]'
        taggedFriendIds = json.dumps(requestData['tagged_friend_ids'])
        timeStamp = requestData['time_stamp']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (commentId, parentId, postId, authorId, content, likes, dislikes, taggedFriendIds, timeStamp))
        commentId = cursor.lastrowid
  
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': commentId, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_posts.route('/posts/sql/add', methods=['POST'])
def addPost():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        authorId = requestData['author_id']
        postContent = requestData['post_content']
        taggedFriendIds = json.dumps(requestData['tagged_friend_ids'])
        timeStamp = requestData['time_stamp']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?)", (None, authorId, postContent, taggedFriendIds, '[]', '[]', timeStamp,))
        postId = cursor.lastrowid
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': {**requestData, 'postId': postId}, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_posts.route('/posts/sql/getAllComments', methods=['POST'])
def getAllComments():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT comments.*, users.first_name, users.last_name FROM comments INNER JOIN users ON comments.author_id = users._ID")
        comments = cursor.fetchall()
        finalComments = []
        for row in comments:
            currentComment = {
                '_ID': row[0],
                'parent_id': row[1],
                'post_id': row[2],
                'author_id': row[3],
                'content': row[4],
                'likes': json.loads(row[5]),
                'dislikes': json.loads(row[6]),
                'tagged_friend_ids': json.loads(row[7]),
                'time_stamp': row[8],
                'first_name': row[9],
                'last_name': row[10]
            }
            finalComments.append(currentComment)
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalComments, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_posts.route('/posts/sql/get', methods=['POST'])
def getAllPosts():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT posts.*, users.first_name, users.last_name FROM posts INNER JOIN users ON posts.author_id = users._ID ORDER BY _ID DESC")
        posts = cursor.fetchall()
        finalPosts = []
        for row in posts:
            currentPost = {
                '_ID': row[0],
                'author_id': row[1],
                'post_content': row[2],
                'tagged_friend_ids': json.loads(row[3]),
                'likes': json.loads(row[4]),
                'dislikes': json.loads(row[5]),
                'timeStamp': row[6],
                'first_name': row[7],
                'last_name': row[8]
            }
            finalPosts.append(currentPost)
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalPosts, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_posts.route('/posts/sql/setCommentLikes', methods=['POST'])
def setCommentLikes():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        commentId = requestData['comment_id']
        likes = requestData['likes']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE comments SET likes = ? WHERE _ID = ?", (json.dumps(likes), commentId,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_posts.route('/posts/sql/setCommentDislikes', methods=['POST'])
def setCommentDislikes():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        commentId = requestData['comment_id']
        dislikes = requestData['dislikes']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE comments SET dislikes = ? WHERE _ID = ?", (json.dumps(dislikes), commentId,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_posts.route('/posts/sql/setPostLikes', methods=['POST'])
def setPostLikes():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        postId = requestData['post_id']
        likes = requestData['likes']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE posts SET likes = ? WHERE _ID = ?", (json.dumps(likes), postId,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_posts.route('/posts/sql/setPostDislikes', methods=['POST'])
def setPostDislikes():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        postId = requestData['post_id']
        dislikes = requestData['dislikes']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE posts SET dislikes = ? WHERE _ID = ?", (json.dumps(dislikes), postId,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})








def socket_init_posts(socketio):
    
    @socketio.on('commentOnComment')
    def commentOnComment(data):
        emit('commentOnComment', data, broadcast=True)
    
    @socketio.on('commentOnPost')
    def commentOnPost(data):
        emit('commentOnPost', data, broadcast=True)
        
    @socketio.on('updateCommentComments')
    def updateCommentComments(data):
        emit('updateCommentComments', data, broadcast=True)
        
    @socketio.on('updatePostComments')
    def updatePostComments(data):
        emit('updatePostComments', data, broadcast=True)
            
    @socketio.on('sendNewPost')
    def sendNewPost(data):
        authorId = data['author_id']
        timeStamp = data['time_stamp']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT posts.*, users.first_name, users.last_name FROM posts INNER JOIN users ON posts.author_id = users._ID WHERE author_id = ? AND time_stamp = ?", (authorId, timeStamp,))
        post = cursor.fetchone()
        if post != None:
            finalPost = {
                '_ID': post[0],
                'author_id': post[1],
                'post_content': post[2],
                'tagged_friend_ids': json.loads(post[3]),
                'likes': json.loads(post[4]),
#                'likes': [int(x) for x in post[5].split(',')] if (post[5] != None and post[5] != '') else [],
                'dislikes': json.loads(post[5]),
                'timeStamp': post[6],
                'first_name': post[7],
                'last_name': post[8]
            }
        sqliteConnection.commit()
        sqliteConnection.close()
        
        emit('receiveNewPost', finalPost, broadcast=True)
        
    @socketio.on('updateCommentLikes')
    def updateCommentLikes(data):
        likeAction = data['action']
        commentId = data['commentId']
        userId = data['userId']
        likeData = {
            'commentId': commentId,
            'userId': userId
        }
        if likeAction == 'add':
            emit('addCommentLike', likeData, broadcast=True)
        elif likeAction == 'remove':
            emit('removeCommentLike', likeData, broadcast=True)
            
    @socketio.on('updateCommentDislikes')
    def updateCommentDislikes(data):
        dislikeAction = data['action']
        commentId = data['commentId']
        userId = data['userId']
        dislikeData = {
            'commentId': commentId,
            'userId': userId
        }
        if dislikeAction == 'add':
            emit('addCommentDislike', dislikeData, broadcast=True)
        elif dislikeAction == 'remove':
            emit('removeCommentDislike', dislikeData, broadcast=True)
        
    @socketio.on('updatePostLikes')
    def updatePostLikes(data):
        likeAction = data['action']
        postId = data['postId']
        userId = data['userId']
        likeData = {
            'postId': postId,
            'userId': userId
        }
        if likeAction == 'add':
            emit('addPostLike', likeData, broadcast=True)
        elif likeAction == 'remove':
            emit('removePostLike', likeData, broadcast=True)
            
    @socketio.on('updatePostDislikes')
    def updatePostDislikes(data):
        dislikeAction = data['action']
        postId = data['postId']
        userId = data['userId']
        dislikeData = {
            'postId': postId,
            'userId': userId
        }
        if dislikeAction == 'add':
            emit('addPostDislike', dislikeData, broadcast=True)
        elif dislikeAction == 'remove':
            emit('removePostDislike', dislikeData, broadcast=True)


            
















    



