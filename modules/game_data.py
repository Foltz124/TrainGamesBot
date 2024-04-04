import json
import sqlite3
import modules.url as URL

BASE_URL = 'https://18xx.games/api/game/'

class GameData:

    def __init__(self):
        self.current_player = None
        self.description = None
        self.id = None
        self.round = None
        self.status = None
        self.title = None
        self.turn = None
        self.updated_at = None

def get_game_data(game_id: int):
    game_data = None

    response = URL.get_response(BASE_URL + str(game_id));
    if response is not None:
        json_response = json.loads(response)
        game_data = GameData()
        game_data.id = game_id
        game_data.title = json_response['title']
        game_data.description = json_response['description']
        game_data.turn = json_response['turn']
        game_data.round = json_response['round']
        game_data.status = json_response['status']
        game_data.current_player = json_response['acting'][0]
        game_data.updated_at = json_response['updated_at']
    return game_data

def _format_string(value: str):
    return '"' + value + '"'

def save_game_data(database, game):
    result = True
    try:
        cursor = database.cursor()
        field_array = [str(game.id), game.title, game.description, str(game.turn), game.round, str(game.current_player), game.status, str(game.updated_at)]
        cursor.execute('INSERT INTO game VALUES(' + ','.join(['?'] * len(field_array)) + ') ON CONFLICT(id) DO UPDATE SET turn=' + str(game.turn) +
                       ', round=' + _format_string(game.round) + ', current_player=' + str(game.current_player) + ', status=' + _format_string(game.status) +
                       ', updated_at= ' + str(game.updated_at), field_array)
        database.commit()
    except Exception as e:
        result = False
        print(e)
    return result

def delete_game_data(database, game):
    result = True
    try:
        cursor = database.cursor()
        cursor.execute('DELETE FROM game WHERE id = ' + str(game.id))
        database.commit()
    except Exception as e:
        result = False
        print(e)
    return result

def get_tracked_games(database):
    result = []
    try:
        cursor = database.cursor()
        for row in cursor.execute('SELECT * from game WHERE status = "active"'):
            current_game = GameData()
            current_game.id = int(row[0])
            current_game.title = row[1]
            current_game.desciption = row[2]
            current_game.turn = int(row[3])
            current_game.round = row[4]
            current_game.current_player = int(row[5])
            current_game.status = row[6]
            current_game.updated_at = row[7]
            result.append(current_game)
    except Exception as e:
        result = None
        print(e)
    return result
