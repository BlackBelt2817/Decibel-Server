import json
import os
import random
import requests
import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
from flask_socketio import emit


curPath = os.path.dirname(__file__)

#explosmPath = curPath + '/../../files/cyanide_and_happiness'

routes_languages = Blueprint('routes_languages', __name__)



    
@routes_languages.route('/languages/sql/cooljugatorAddTranslations', methods=['POST'])
def cooljugatorAddTranslations():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        translations = requestData['translations']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        
        for translation in translations:
            language_abbreviation = translation['lang_abbr']
            infinitive_foreign = translation['inf_for']
            infinitive_english = translation['inf_eng']
            translation_tables = translation['transl_tables']
            cursor.execute("INSERT INTO cooljugator (_ID, language_abbreviation, infinitive_foreign, infinitive_english, translation_tables) VALUES(?, ?, ?, ?, ?)", (None, language_abbreviation, infinitive_foreign, infinitive_english, translation_tables,))
            sqliteConnection.commit()

        sqliteConnection.close()
        
        return jsonify({'data': translations, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_languages.route('/languages/sql/get/cooljugatorTranslationsByAbbreviation', methods=['POST'])
def cooljugatorTranslationsByAbbreviation():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        abbreviation = requestData['abbreviation']

        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM cooljugator WHERE language_abbreviation = ? ORDER BY infinitive_foreign", (abbreviation,))
        translations = cursor.fetchall()
        
        sqliteConnection.commit()
        sqliteConnection.close()
        
        if len(translations) < 1:
            return jsonify({'data': [], 'success': True})
        else:
            finalTranslations = []
            for translation in translations:
                currentTranslation = {
                    '_ID': translation[0],
                    'languageAbbreviation': translation[1],
                    'infinitiveForeign': translation[2],
                    'infinitiveEnglish': translation[3],
                    'translationTables': json.loads(translation[4])
                    
                }
                finalTranslations.append(currentTranslation)
            return jsonify({'data': finalTranslations, 'success': True})
    
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    

    




    
    
        
        



















