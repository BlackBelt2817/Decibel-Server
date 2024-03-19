import json
import os
import random
import requests
import sqlite3
from flask import Blueprint, jsonify, request, Response, send_file
from flask_socketio import emit


curPath = os.path.dirname(__file__)

explosmPath = curPath + '/../../files/cyanide_and_happiness'

routes_games = Blueprint('routes_games', __name__)

@routes_games.route('/games/sql/create', methods=['POST'])
def createGame():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        gameData = requestData['gameData']
        gameName = requestData['gameName']
        chatId = None
        if gameName == 'Explosm':
            cardsInDeck = gameData['cardsInDeck']
            cardsInHand = gameData['cardsInHand']
            cardsInPlay = gameData['cardsInPlay']
            cardsPlayed = gameData['cardsPlayed']
            chatId = requestData['chatId']
            currentTurnUserId = gameData['currentTurnUserId']
            judge = gameData['judge']
            gameStatus = gameData['gameStatus']
            roundStatus = gameData['roundStatus']
            selectedWinningCard = gameData['selectedWinningCard']
            turnsTaken = gameData['turnsTaken']
            userIds = requestData['userIds']
            usersToContinue = gameData['usersToContinue']
            winnerId = gameData['winnerId']
            winners = gameData['winners']
            
            explosmDir = os.listdir(explosmPath)
#            for deck in cardsInDeck:
#                for card in cardsInDeck[deck]:
#                    if card not in explosmDir:
#                        url = 'https://rcg-cdn.explosm.net/panels/' + card
#                        page = requests.get(url)
#                        ext = os.path.splitext(url)[-1]
#                        with open(os.path.join('../files/cyanide_and_happiness', card), 'wb') as f:
#                            f.write(page.content)
            for card in cardsInDeck:
                if card not in explosmDir:
                    url = 'https://rcg-cdn.explosm.net/panels/' + card
                    page = requests.get(url)
                    ext = os.path.splitext(url)[-1]
                    with open(os.path.join('../files/cyanide_and_happiness', card), 'wb') as f:
                        f.write(page.content)
            
            gameData = {
                'cardsInDeck': cardsInDeck,
                'cardsInHand': cardsInHand,
                'cardsInPlay': cardsInPlay,
                'cardsPlayed': cardsPlayed,
                'currentTurnUserId': currentTurnUserId,
                'judge': judge,
#                0: started
#                1: finished
                'gameStatus': gameStatus,
#                0: playing
#                1: finished
                'roundStatus': roundStatus,
                'selectedWinningCard': selectedWinningCard,
                'turnsTaken': turnsTaken,
                'usersToContinue': usersToContinue,
                'winnerId': winnerId,
                'winners': winners
            }
        elif gameName == 'Solitaire':
            chatId = requestData['chatId']
            
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO games VALUES (?, ?, ?, ?)", (None, chatId, gameName, json.dumps(gameData),))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/explosmAddCardsToDeck', methods=['POST'])
def explosmAddCardsToDeck():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        cards = requestData['cards']
        chatId = requestData['chatId']
        
        explosmDir = os.listdir(explosmPath)
        for card in cards:
            if card not in explosmDir:
                url = 'https://rcg-cdn.explosm.net/panels/' + card
                page = requests.get(url)
                ext = os.path.splitext(url)[-1]
                with open(os.path.join('../files/cyanide_and_happiness', card), 'wb') as f:
                    f.write(page.content)
                
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ?", (chatId,))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        cardsInDeck = updatedGameData['cardsInDeck']
        for card in cards:
            cardsInDeck.append(card)
        
        updatedGameData['cardsInDeck'] = cardsInDeck

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Explosm',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': cards, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/explosmChooseWinningCard', methods=['POST'])
def explosmChooseWinningCard():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        chatId = requestData['chatId']
#        newJudge = requestData['newJudge']
        selectedWinningCard = requestData['selectedWinningCard']
        winnerId = requestData['winnerId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? and game_name = ?", (chatId, 'Explosm',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        updatedGameData['selectedWinningCard'] = selectedWinningCard
        if selectedWinningCard not in updatedGameData['winners'][str(winnerId)]:
            updatedGameData['winners'][str(winnerId)].append(selectedWinningCard)
        updatedGameData['winnerId'] = winnerId
#        updatedGameData['judge'] = newJudge
#        updatedGameData['currentTurnUserId'] = newJudge

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Explosm',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/explosmContinueGame', methods=['POST'])
def explosmContinueGame():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        
        chatId = requestData['chatId']
        newJudge = requestData['newJudge']
        selectedWinningCard = requestData['selectedWinningCard']
        userId = requestData['userId']
        userIdCount = requestData['userIdCount']
        winnerId = requestData['winnerId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? and game_name = ?", (chatId, 'Explosm',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        if userId not in updatedGameData['usersToContinue']:
            updatedGameData['usersToContinue'].append(userId)
            
        if len(updatedGameData['usersToContinue']) == userIdCount:
            cardsPlayed = updatedGameData['cardsPlayed']
            cardsInPlay = updatedGameData['cardsInPlay']
            cardsInDeck = updatedGameData['cardsInDeck']
            for user in cardsInPlay:
                for card in cardsInPlay[user]:
                    if card not in cardsPlayed:
                        cardsPlayed.append(card)
                cardsInPlay[user].clear()
            cardsInPlay[str(newJudge)].append(cardsInDeck[0])
            cardsInDeck.pop(0)
            updatedGameData['cardsPlayed'] = cardsPlayed
            updatedGameData['cardsInPlay'] = cardsInPlay
            if not selectedWinningCard in updatedGameData['turnsTaken'][str(winnerId)]:
                updatedGameData['turnsTaken'][str(winnerId)].append(selectedWinningCard)
            updatedGameData['usersToContinue'] = []
            updatedGameData['winnerId'] = -1
            if not selectedWinningCard in updatedGameData['winners'][str(winnerId)]:
                updatedGameData['winners'][str(winnerId)].append(selectedWinningCard)
            updatedGameData['judge'] = newJudge
            updatedGameData['currentTurnUserId'] = newJudge
            

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Explosm',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': updatedGameData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/explosmDrawCard', methods=['POST'])
def explosmDrawCard():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        gameName = requestData['gameName']
        userId = requestData['userId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? AND game_name = ?", (chatId, gameName,))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        cardsInDeck = updatedGameData['cardsInDeck']
        cardsInHand = updatedGameData['cardsInHand']
        
        cardToDraw = cardsInDeck[0]
        cardsInDeck.pop(0)
        cardsInHand[str(userId)].append(cardToDraw)
        
        updatedGameData['cardsInDeck'] = cardsInDeck
        updatedGameData['cardsInHand'] = cardsInHand

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, gameName,))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': cardToDraw, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/files/get/allExplosmCards', methods=['GET'])
def explosmGetAllCards():
    try:
        explosmDir = os.listdir(explosmPath)
        random.shuffle(explosmDir)
        return jsonify({'data': explosmDir, 'success': True,})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/files/get/explosmCardImage/<card>', methods=['GET'])
def explosmGetCardImage(card):
    try:
        return send_file(os.path.join(explosmPath, card))
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/explosmPlayCardFromHand', methods=['POST'])
def explosmPlayCardFromHand():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        cardIndex = requestData['cardIndex']
        cardPosition = requestData['cardPosition']
        chatId = requestData['chatId']
        userId = requestData['userId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? and game_name = ?", (chatId, 'Explosm',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        cardToPlay = updatedGameData['cardsInHand'][str(userId)][cardIndex]
        updatedGameData['cardsInHand'][str(userId)].pop(cardIndex)
        updatedGameData['cardsPlayed'].append(cardToPlay)
        
        if cardPosition == None or cardPosition == 'right':
            updatedGameData['cardsInPlay'][str(userId)].append(cardToPlay)
        else:
            updatedGameData['cardsInPlay'][str(userId)].insert(0, cardToPlay)

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Explosm',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/explosmPlayJudgeCard', methods=['POST'])
def explosmPlayJudgeCard():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        deckNumber = requestData['deckNumber']
        gameName = requestData['gameName']
        userId = requestData['userId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? and game_name = ?", (chatId, 'Explosm',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        cardToPlay = updatedGameData['cardsInDeck'][str(deckNumber)][0]
        updatedGameData['cardsInDeck'][str(deckNumber)].pop(0)
        updatedGameData['cardsInPlay'][str(userId)].append(cardToPlay)
        updatedGameData['cardsPlayed'].append(cardToPlay)

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Explosm',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/explosmSetGameState', methods=['POST'])
def explosmSetGameState():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        currentTurnUserId = requestData['currentTurnUserId']
        gameStatus = requestData['gameStatus']
        roundStatus = requestData['roundStatus']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? and game_name = ?", (chatId, 'Explosm',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        updatedGameData['currentTurnUserId'] = currentTurnUserId
        updatedGameData['gameStatus'] = gameStatus
        updatedGameData['roundStatus'] = roundStatus

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Explosm',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})

@routes_games.route('/games/sql/get/byUserId', methods=['POST'])
def getGamesByUserId():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        userId = requestData['userId']
        userIdNeg = userId * -1
#        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
#        cursor.execute("SELECT * FROM games WHERE chat_id = ?", (chatId,))
        cursor.execute("SELECT * FROM chats WHERE user_ids = ? OR user_ids LIKE ? OR user_ids LIKE ? OR user_ids LIKE ?", ('[' + str(userId) + ']', '%, ' + str(userId) + ',%', '[' + str(userId) + ', %', '%, ' + str(userId) + ']'))
        chatIds = cursor.fetchall()
        allChatIds = []
        
        if len(chatIds) < 1:
            return jsonify({'data': [], 'success': True})
        else:
            for chatId in chatIds:
                allChatIds.append(chatId[0])
        
        sqlExecStatement = "SELECT * FROM games WHERE chat_id == {uin} OR chat_id IN ({seq})".format(uin=str(userIdNeg), seq=','.join(['?']*len(allChatIds)))
        cursor.execute(sqlExecStatement, allChatIds)
        games = cursor.fetchall()
        
        sqliteConnection.commit()
        sqliteConnection.close()
        
        finalGames = []
        
        if len(games) < 1:
            return jsonify({'data': [], 'success': True})
        else:
            for game in games:
                currentGame = {
                    '_ID': game[0],
                    'chatId': game[1],
                    'gameName': game[2],
                    'gameData': json.loads(game[3])
                }
                finalGames.append(currentGame)
            return jsonify({'data': finalGames, 'success': True})
    
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/solitaireDeleteGame', methods=['POST'])
def solitaireDeleteGame():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("DELETE from games WHERE chat_id = ? AND game_name = ?", (chatId, 'Solitaire',))
        
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/solitaireDiscardPileAddCardFromFaceUp', methods=['POST'])
def solitaireDiscardPileAddCardFromFaceUp():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? AND game_name = ?", (chatId, 'Solitaire',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        faceUpCard = updatedGameData['faceUp'][-1]
        faceUpCard['faceUp'] = '1'
        updatedGameData['faceUp'].pop(-1)
        
        suit = faceUpCard['suit']
        if suit == 'clubs':
            updatedGameData['clubs'].insert(0, faceUpCard)
        elif suit == 'diamonds':
            updatedGameData['diamonds'].insert(0, faceUpCard)
        elif suit == 'hearts':
            updatedGameData['hearts'].insert(0, faceUpCard)
        elif suit == 'spades':
            updatedGameData['spades'].insert(0, faceUpCard)

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Solitaire',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': updatedGameData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/solitaireDiscardPileAddCardFromStack', methods=['POST'])
def solitaireDiscardPileAddCardFromStack():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        fromIndex = requestData['fromIndex']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? AND game_name = ?", (chatId, 'Solitaire',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        draggedCard = updatedGameData['stacks'][str(fromIndex)][-1]
        updatedGameData['stacks'][str(fromIndex)].pop()
        draggedCard['faceUp'] = '1'
        if len(updatedGameData['stacks'][str(fromIndex)]) > 0:
            updatedGameData['stacks'][str(fromIndex)][-1]['faceUp'] = '1'
        
        suit = draggedCard['suit']
        if suit == 'clubs':
            updatedGameData['clubs'].insert(0, draggedCard)
        elif suit == 'diamonds':
            updatedGameData['diamonds'].insert(0, draggedCard)
        elif suit == 'hearts':
            updatedGameData['hearts'].insert(0, draggedCard)
        elif suit == 'spades':
            updatedGameData['spades'].insert(0, draggedCard)

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Solitaire',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': updatedGameData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/solitaireDragCardsFromDifferentStack', methods=['POST'])
def solitaireDragCardsFromDifferentStack():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        cardsLength = requestData['cardsLength']
        fromIndex = requestData['fromIndex']
        toIndex = requestData['toIndex']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? AND game_name = ?", (chatId, 'Solitaire',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        draggedCards = updatedGameData['stacks'][str(fromIndex)][-cardsLength:]
        del updatedGameData['stacks'][str(fromIndex)][-cardsLength:]
        if len(updatedGameData['stacks'][str(fromIndex)]) > 0:
            updatedGameData['stacks'][str(fromIndex)][-1]['faceUp'] = '1'
        updatedGameData['stacks'][str(toIndex)].extend(draggedCards)

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Solitaire',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': updatedGameData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/solitaireDrawCard', methods=['POST'])
def solitaireDrawCard():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? AND game_name = ?", (chatId, 'Solitaire',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        remainingDeck = updatedGameData['remainingDeck']
        faceUp = updatedGameData['faceUp']
        
        if len(remainingDeck) < 1:
            remainingDeck = faceUp
            faceUp = []
        else:
            cardToDraw = remainingDeck[0]
            remainingDeck.pop(0)
            faceUp.append(cardToDraw)
        
        updatedGameData['remainingDeck'] = remainingDeck
        updatedGameData['faceUp'] = faceUp

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Solitaire',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': updatedGameData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/solitaireEmptyStackAddKingFromFaceUp', methods=['POST'])
def solitaireEmptyStackAddKingFromFaceUp():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        stackIndex = requestData['stackIndex']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? AND game_name = ?", (chatId, 'Solitaire',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        faceUpCard = updatedGameData['faceUp'][-1]
        faceUpCard['faceUp'] = '1'
        updatedGameData['faceUp'].pop(-1)
        
        updatedGameData['stacks'][str(stackIndex)] = [faceUpCard]

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Solitaire',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': updatedGameData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/solitaireSetGameState', methods=['POST'])
def solitaireSetGameState():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        gameStatus = requestData['gameStatus']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? and game_name = ?", (chatId, 'Solitaire',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        updatedGameData['gameStatus'] = gameStatus

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Solitaire',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': requestData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/solitaireStackAddCardFromFaceUp', methods=['POST'])
def solitaireStackAddCardFromFaceUp():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        chatId = requestData['chatId']
        stackIndex = requestData['stackIndex']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT game_data from games WHERE chat_id = ? AND game_name = ?", (chatId, 'Solitaire',))
        
        oldGameData = cursor.fetchone()[0]
        updatedGameData = json.loads(oldGameData)
        
        faceUpCard = updatedGameData['faceUp'][-1]
        faceUpCard['faceUp'] = '1'
        updatedGameData['faceUp'].pop(-1)
        
        updatedGameData['stacks'][str(stackIndex)].append(faceUpCard)

        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Solitaire',))
        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': updatedGameData, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    
@routes_games.route('/games/sql/triviaQuestionsSendToServer', methods=['POST'])
def triviaQuestionsSendToServer():
    try:
        requestJson = request.get_json()
        requestData = requestJson['data']
        questionsFromClient = requestData['questions']
        
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * from trivia_questions", ())
        questionsFromServer = cursor.fetchall()
        formattedQuestionsFromServer = {}
        
        for serverQuestion in questionsFromServer:
            formattedQuestionsFromServer[serverQuestion[1]] = {
                'category': serverQuestion[2],
                'question': serverQuestion[3],
                'correctAnswer': serverQuestion[4],
                'incorrectAnswers': serverQuestion[5],
                'tags': serverQuestion[6],
                'questionType': serverQuestion[7],
                'difficulty': serverQuestion[8],
                'regions': serverQuestion[9],
                'isNiche': serverQuestion[10]
            }
#            print(serverQuestion)
        
        for questionFromClient in questionsFromClient:
#            foundQuestion = formattedQuestionsFromServer[question['id']]
            foundQuestion = formattedQuestionsFromServer.get(questionFromClient['id'])
            if foundQuestion == None:
#                print(questionFromClient)
                _ID = None
                questionId = questionFromClient['id']
                category = questionFromClient['category']
                question = questionFromClient['question']
                correctAnswer = questionFromClient['correctAnswer']
                incorrectAnswers = json.dumps(questionFromClient['incorrectAnswers'])
                tags = json.dumps(questionFromClient['tags'])
                questionType = questionFromClient['type']
                difficulty = None if questionFromClient.get('difficulty') == None else questionFromClient.get('difficulty')
                regions = json.dumps(questionFromClient['regions'])
                isNiche = 1 if questionFromClient['isNiche'] == True else 0
#                print(questionFromClient)
                cursor.execute("INSERT INTO trivia_questions(_ID, question_id, category, question, correct_answer, incorrect_answers, tags, question_type, difficulty, regions, is_niche) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (_ID, questionId, category, question, correctAnswer, incorrectAnswers, tags, questionType, difficulty, regions, isNiche,))
                sqliteConnection.commit()

        print('Trivia Questions saved!')
#        
#        oldGameData = cursor.fetchone()[0]
#        updatedGameData = json.loads(oldGameData)
#        
#        updatedGameData['gameStatus'] = gameStatus
#
#        cursor.execute("UPDATE games SET game_data = ? WHERE chat_id = ? AND game_name = ?", (json.dumps(updatedGameData), chatId, 'Solitaire',))
#        sqliteConnection.commit()
        sqliteConnection.close()
        
        return jsonify({'data': questionsFromServer, 'success': True})
    except Exception as e:
        return jsonify({'data': None, 'success': False, 'error': e})
    

    




def socket_init_games(socketio):
    
    @socketio.on('createGame')
    def createGame(data):
        emit('createGame', data, broadcast=True)
    
    @socketio.on('explosmAddCardsToGame')
    def explosmAddCardsToGame(data):
        emit('explosmAddCardsToGame', data, broadcast=True)
        
    @socketio.on('explosmChooseWinningCard')
    def explosmChooseWinningCard(data):
        emit('explosmChooseWinningCard', data, broadcast=True)
        
    @socketio.on('explosmContinueGame')
    def explosmContinueGame(data):
        emit('explosmContinueGame', data, broadcast=True)

    @socketio.on('explosmDrawCard')
    def explosmDrawCard(data):
        emit('explosmDrawCard', data, broadcast=True)

    @socketio.on('explosmPlayCardFromHand')
    def explosmPlayCardFromHand(data):
        emit('explosmPlayCardFromHand', data, broadcast=True)
        
    @socketio.on('explosmPlayDeckCard')
    def explosmPlayDeckCard(data):
        emit('explosmPlayDeckCard', data, broadcast=True)

    
    
        
        


















