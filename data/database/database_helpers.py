import sqlite3
from pathlib import Path
from datetime import datetime

database_path = (Path(__file__).parent / './database.db').resolve()

def insert_into_games(game_entry):
    connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    game_entry = (*game_entry, datetime.now())

    cursor.execute('''
        INSERT INTO games (cpu_enabled, cpu_depth, winner, time_enabled, time, number_of_ply, moves, fen_string, created_dt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', game_entry)

    games = cursor.execute('''
        SELECT * FROM games
    ''')

    print('(database_helpers.insert_into_games) Games database entries:')

    connection.commit()
    connection.close()

def get_all_games():
    connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
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

def delete_game(id):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM games WHERE id = ?
    ''', (id,))

    connection.commit()
    connection.close()

def get_ordered_games(column, ascend=True):
    connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if ascend:
        ascend_arg = 'ASC'
    else:
        ascend_arg = 'DESC'

    cursor.execute(f'''
        SELECT * FROM games ORDER BY {column} {ascend_arg}
    ''')
    games = cursor.fetchall()

    connection.close()

    return [dict(game) for game in games]

# delete_all_games()