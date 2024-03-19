import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())
    
#with open('backup.sql') as b:
#    connection.executescript(b.read())
    
#cur = connection.cursor()

connection.commit()
connection.close