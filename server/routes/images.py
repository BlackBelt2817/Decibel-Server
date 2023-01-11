import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
import os
#from werkzeug.utils import secure_filename

curPath = os.path.dirname(__file__)

musicPath = curPath + '/../../files/music'

imagesPath = curPath + '/../../files/images'
headerImagesPath = imagesPath + '/Header Images'
headerImageThumbnailsPath = imagesPath + '/Header Image Thumbnails'
songArtImagesPath = imagesPath + '/Song Art Images'
songArtImageThumbnailsPath = imagesPath + '/Song Art Image Thumbnails'
#imagesDir = os.listdir(songArtImageThumbnailsPath)

routes_images = Blueprint('routes_images', __name__)

@routes_images.route('/images/files/getMissing/post', methods=['POST'])
def getMissingImageIds():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        idsList = requestData['ids_list']
        
        headerImagesDir = os.listdir(headerImagesPath)
        headerImageThumbnailsDir = os.listdir(headerImageThumbnailsPath)
        songArtImagesDir = os.listdir(songArtImagesPath)
        songArtImageThumbnailsDir = os.listdir(songArtImageThumbnailsPath)
        
        finalHeaderImageIds = []
        finalHeaderImageThumbnailIds = []
        finalSongArtImageIds = []
        finalSongArtImageThumbnailIds = []
        finalIds = []
        
        for songId in idsList:
            finalHeaderImageIds.append(songId)
            finalHeaderImageThumbnailIds.append(songId)
            finalSongArtImageIds.append(songId)
            finalSongArtImageThumbnailIds.append(songId)
            
        for songId in idsList:
            for headerImage in headerImagesDir:
                if songId in headerImage:
                    finalHeaderImageIds.remove(songId)
            for headerImageThumbnail in headerImageThumbnailsDir:
                if songId in headerImageThumbnail:
                    finalHeaderImageThumbnailIds.remove(songId)
            for songArtImage in songArtImagesDir:
                if songId in songArtImage:
                    finalSongArtImageIds.remove(songId)
            for songArtImageThumbnail in songArtImageThumbnailsDir:
                if songId in songArtImageThumbnail:
                    finalSongArtImageThumbnailIds.remove(songId)
                    
        for songId in finalHeaderImageIds:
            if songId not in finalIds:
                finalIds.append(songId)
        for songId in finalHeaderImageThumbnailIds:
            if songId not in finalIds:
                finalIds.append(songId)
        for songId in finalSongArtImageIds:
            if songId not in finalIds:
                finalIds.append(songId)
        for songId in finalSongArtImageThumbnailIds:
            if songId not in finalIds:
                finalIds.append(songId)

        return jsonify({'data': finalIds, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_images.route('/images/file/upload', methods=['POST'])
def uploadImageFile():
    try:
        requestForm = request.form
        
        songId = requestForm['song_id']
        folder = requestForm['folder']
        extension = requestForm['extension']
        imageFile = request.files['image_file']
        
        imageFile.save(os.path.join('../files/images' + folder, songId + '.' + extension))
        
        return jsonify({'data': None, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    

