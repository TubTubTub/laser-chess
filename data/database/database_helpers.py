import sqlite3
from pathlib import Path

database_path = (Path(__file__).parent / './database.db').resolve()

def insert_into_games(game_entry):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO games (cpu_enabled, cpu_depth, winner, time_enabled, time, number_of_ply, moves, fen_string)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    ''', game_entry)

    games = cursor.execute('''
        SELECT * FROM games
    ''')

    print('(database_helpers.insert_into_games) Games database entries:')
    for game in games.fetchall():
        print(game)

    connection.commit()
    connection.close()

def get_all_games():
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM games
    ''')
    games = cursor.fetchall()

    connection.close()

    return [dict(game) for game in games]

def delete_all_games():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM games
    ''')

    connection.commit()
    connection.close()