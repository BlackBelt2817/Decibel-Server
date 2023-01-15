import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
import os
#from pytube import YouTube

curPath = os.path.dirname(__file__)

musicPath = curPath + '/../../files/music'

routes_songs = Blueprint('routes_songs', __name__)

@routes_songs.route('/songs/sql/delete/<songId>', methods=['DELETE'])
def deleteSongSqlById(songId):
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("DELETE FROM songs WHERE song_id = ?", (songId,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': 'songId', 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_songs.route('/songs/files/getMissing/post', methods=['POST'])
def getMissingSongIds():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        idsList = requestData['ids_list']
        
        songsPath = curPath + '/../../files/music'
        songsDir = os.listdir(songsPath)
        
        if len(songsDir) < 1:
            return jsonify({'data': idsList, 'success': True})
        else:
            finalIds = []
            for songId in idsList:
                finalIds.append(songId)
            for songId in idsList:
                for song in songsDir:
                    if songId in song:
                        finalIds.remove(songId)
            return jsonify({'data': finalIds, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_songs.route('/songs/file/get/<fileName>', methods=['GET'])
def getSongFile(fileName):
    try:
        musicDir = os.listdir(musicPath)
        return send_file(os.path.join(musicPath, fileName))
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_songs.route('/songs/files/get/fileNames', methods=['GET'])
def getSongFileNames():
    try:
        musicDir = os.listdir(musicPath)
        return jsonify({'data': musicDir, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_songs.route('/songs/sql/get/album', methods=['GET'])
def getSongsSqlSortedByAlbum():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM songs ORDER BY album COLLATE NOCASE ASC, artist COLLATE NOCASE ASC, CAST(track as INTEGER) ASC")
        songs = cursor.fetchall()
        finalSongs = []
        for row in songs:
            currentSong = {
                '_ID': row[0],
                'song_id': row[1],
                'artist': row[2],
                'title': row[3],
                'album': row[4],
                'lyrics': row[5],
                'extension': row[6],
                'track': row[7],
                'file_downloaded': row[8],
                'record_verified': row[9],
                'lyrics_link': row[10]
            }
            finalSongs.append(currentSong)
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalSongs, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_songs.route('/songs/sql/get/artist', methods=['GET'])
def getSongsSqlSortedByArtist():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM songs ORDER BY artist COLLATE NOCASE ASC, album COLLATE NOCASE ASC, CAST(track as INTEGER) ASC")
        songs = cursor.fetchall()
        finalSongs = []
        for row in songs:
            currentSong = {
                '_ID': row[0],
                'song_id': row[1],
                'artist': row[2],
                'title': row[3],
                'album': row[4],
                'lyrics': row[5],
                'extension': row[6],
                'track': row[7],
                'file_downloaded': row[8],
                'record_verified': row[9],
                'lyrics_link': row[10]
            }
            finalSongs.append(currentSong)
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalSongs, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_songs.route('/songs/sql/get', methods=['GET'])
def getSongsSqlSortedByTitle():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM songs ORDER BY title COLLATE NOCASE ASC")
        songs = cursor.fetchall()
        finalSongs = []
        for row in songs:
            currentSong = {
                '_ID': row[0],
                'song_id': row[1],
                'artist': row[2],
                'title': row[3],
                'album': row[4],
                'lyrics': row[5],
                'extension': row[6],
                'track': row[7],
                'file_downloaded': row[8],
                'record_verified': row[9],
                'lyrics_link': row[10]
            }
            finalSongs.append(currentSong)
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': finalSongs, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_songs.route('/songs/sql/patch/extension', methods=['PATCH'])
def updateSongSqlExtension():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        songId = requestData['song_id']
        extension = requestData['extension']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE songs SET extension = ? WHERE song_id = ?", (extension, songId,))
        sqliteConnection.commit()
        sqliteConnection.close()

        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_songs.route('/songs/sql/patch', methods=['PATCH'])
def updateSongSqlOne():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        songId = requestData['song_id']
        artist = requestData['artist']
        title = requestData['title']
        album = requestData['album']
        track = requestData['track']
        geniusLink = requestData['genius_link']
        lyrics = requestData['lyrics']
        fileDownloaded = requestData['file_downloaded']
        recordVerified = requestData['record_verified']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE songs SET artist = ?, title = ?, album = ?, lyrics = ?, track = ?, file_downloaded = ?, record_verified = ?, lyrics_link = ? WHERE song_id = ?", (artist, title, album, lyrics, track, fileDownloaded, recordVerified, geniusLink, songId,))
        sqliteConnection.commit()
        sqliteConnection.close()

        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_songs.route('/songs/file/upload', methods=['POST'])
def uploadSongFile():
    try:
        requestForm = request.form
        
        songId = requestForm['song_id']
        extension = requestForm['extension']
        songFile = request.files['song_file']
        
        songFile.save(os.path.join('../files/music', songId + '.' + extension))
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE songs SET file_downloaded = ?, extension = ? WHERE song_id = ?", (1, extension, songId,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': None, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_songs.route('/songs/sql/jsonArray/post', methods=['POST'])
def uploadSongSql():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        for song in requestData:
            songId = song['song_id']
            artist = song['artist']
            title = song['title']
            lyrics = song['lyrics']
            lyricsLink = song['lyrics_link']
            extension = song['extension']
            album = song['album']
            track = song['track']
        
            sqliteConnection = sqlite3.connect('database.db')
            cursor = sqliteConnection.cursor()
            cursor.execute("INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, songId, artist, title, album, lyrics, extension, track, 0, 0, lyricsLink))
            sqliteConnection.commit()
            sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

