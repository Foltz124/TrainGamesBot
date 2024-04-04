import sqlite3

def save_player(database, player_id, discord_id):
    result = True
    try:
        cursor = database.cursor()
        cursor.execute('INSERT INTO player VALUES(' + str(player_id) + ', "' + str(discord_id) + '")')
        database.commit()
    except Exception as e:
        result = False
        print(e)
    return result

def delete_player(database, player_id):
    result = True
    try:
        cursor = database.cursor()
        cursor.execute("DELETE FROM player WHERE id = " + str(player_id))
        database.commit()
    except Exception as e:
        result = False
        print(e)
    return result

def get_discord_id(database, player_id):
    result = None
    try:
        cursor = database.cursor()
        cursor.execute("SELECT * from player WHERE id = " + str(player_id));
        database_tuple = cursor.fetchone()
        if database_tuple is not None:
            result = database_tuple[1]
    except Exception as e:
        print(e)
    return result

