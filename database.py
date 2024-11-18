import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# cursor.execute('''
# CREATE TABLE moves(hi, geat, be)
# ''')

cursor.execute('''
INSERT INTO moves VALUES
               ('aa', 3 ,3.2)
''')

connection.commit()

result = cursor.execute('SELECT * from moves')
result.fetchall()