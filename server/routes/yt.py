import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
import os
from pytube import YouTube
import youtube_dl
from flask_socketio import emit, send

curPath = os.path.dirname(__file__)

musicPath = curPath + '/../../files/music'

routes_yt = Blueprint('routes_yt', __name__)

#socket = None

downloads = {}

#def downloadProgressHook(d):
#    if d['status'] ==
def updateDownloads(d):
#    print(d)
    filename = d['filename'].split('/')[-1]
    songId = filename.split('.')[0]
    extension = filename.split('.')[1]
    progress = 0
    if d['status'] == 'downloading':
        progress = round(float(''.join(d['_percent_str'].split('%'))))
    else:
        progress = 100
    downloads[songId] = {
        'progress': progress,
        'extension': extension
    }
    print(songId + '.' + downloads[songId]['extension'] + ': ' + str(downloads[songId]['progress']) + '%')
#    send('updateDownloadProgress', downloads, namespace='/yt')
#    emit('fuck', {'shit':'AHHH'}, broadcast=True)
#    if d['status'] == 'finished':
#        
#    print(d['_percent_str'])

@routes_yt.route('/yt/audio/download', methods=['POST'])
def downloadYtAudio():
    try:
        requestJson = request.get_json()
        ytLink = requestJson['ytLink']
        
        options = {
            'outtmpl': os.path.join('../files/music', '%(id)s.%(ext)s'),
#            'outtmpl':  '%s/%(id)s.%(ext)s' % os.path.join('../files/music'),
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp4',
            'progress_hooks': [updateDownloads]
        }
        ytdl = youtube_dl.YoutubeDL(options)
        with ytdl:
            ytdl.download([ytLink])
#            result = ytdl.extract_info(ytLink, download=False)
        
#        if 'entries' in result:
#            video = result['entries']
#        else:
#            video = result        

#        return result
#        return jsonify({'ytlink': ytLink})
#        return requestJson
        return requestJson
    except Exception as e:
#        pass
        print(e)
        return jsonify({'data': None, 'success': False, 'error': e})

#@routes_yt.route('/yt/file/download', methods=['POST'])
#def downloadYtFile():
#    try:
#        requestJson = request.get_json()
##        requestData = requestJson['data']
#        
#        ytLink = requestJson['ytLink']
#        
#        video = YouTube(ytLink)
#        audio = video.streams.filter(only_audio=True).first()
#        
##        yt = YouTube(ytLink)
##        title = yt.title
##        s = yt.streams
##        for x in s:
##            print(x)
##        yt.streams.filter(file_extension='mp4')
##        
##        youtubeObject = YouTube(ytLink)
##        youtubeObjectToDownload = youtubeObject.streams.get_highest_resolution()
##        youtubeObjectToDownload.download()
#
#        return jsonify({'data': ytLink, 'success': True})
#    except Exception as e:
##        pass
#        print(e)
#        return jsonify({'data': None, 'success': False, 'error': e})
    
    
    
    
def socket_init_yt(socketio):
    
    @socketio.on('updateDownloadProgress')
    def updateDownloadProgress(data):
        print('FUCK')
        emit('updateDownloadProgress', data, broadcast=True)    
    
