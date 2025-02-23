import sqlite3
from pathlib import Path
from datetime import datetime

database_path = (Path(__file__).parent / '../database/database.db').resolve()

def insert_into_games(game_entry):
    """
    Inserts a new row into games table.

    Args:
        game_entry (GameEntry): GameEntry object containing game information.
    """
    connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    # Datetime added for created_dt column
    game_entry = (*game_entry, datetime.now())

    cursor.execute('''
        INSERT INTO games (cpu_enabled, cpu_depth, winner, time_enabled, time, number_of_ply, moves, start_fen_string, final_fen_string, created_dt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', game_entry)

    connection.commit()
    connection.close()

def get_all_games():
    """
    Get all rows in games table.

    Returns:
        list[dict]: List of game entries represented as dictionaries.
    """
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
    """
    Delete all rows in games table.
    """
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM games
    ''')

    connection.commit()
    connection.close()

def delete_game(id):
    """
    Deletes specific row in games table using id attribute.

    Args:
        id (int): Primary key for row.
    """
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM games WHERE id = ?
    ''', (id,))

    connection.commit()
    connection.close()

def get_ordered_games(column, ascend=True, start_row=1, end_row=10):
    """
    Get specific number of rows from games table ordered by a specific column(s).

    Args:
        column (_type_): Column to sort by.
        ascend (bool, optional): Sort ascending or descending. Defaults to True.
        start_row (int, optional): First row returned. Defaults to 1.
        end_row (int, optional): Last row returned. Defaults to 10.

    Raises:
        ValueError: If ascend argument or column argument are invalid types.

    Returns:
        list[dict]: List of ordered game entries represented as dictionaries.
    """
    if not isinstance(ascend, bool) or not isinstance(column, str):
        raise ValueError('(database_helpers.get_ordered_games) Invalid input arguments!')

    connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    # Match ascend bool to correct SQL keyword
    if ascend:
        ascend_arg = 'ASC'
    else:
        ascend_arg = 'DESC'
    
    # Partition by winner, then order by time and number_of_ply
    if column == 'winner':
        cursor.execute(f'''
            SELECT * FROM
                (SELECT ROW_NUMBER() OVER (
                    PARTITION BY winner
                    ORDER BY time {ascend_arg}, number_of_ply {ascend_arg}
                ) AS row_num, * FROM games)
            WHERE row_num >= ? AND row_num <= ?
        ''', (start_row, end_row))
    else:
    # Order by time or number_of_ply only
        cursor.execute(f'''
            SELECT * FROM
                (SELECT ROW_NUMBER() OVER (
                    ORDER BY {column} {ascend_arg}
                ) AS row_num, * FROM games)
            WHERE row_num >= ? AND row_num <= ?
        ''', (start_row, end_row))

    games = cursor.fetchall()

    connection.close()

    return [dict(game) for game in games]

def get_number_of_games():
    """
    Returns:
        int: Number of rows in the games.
    """
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(ROWID) FROM games
    """)

    result = cursor.fetchall()[0][0]

    connection.close()

    return result

# delete_all_games()