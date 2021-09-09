import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
cursor.execute(create_table_query)

item_table = "CREATE TABLE IF NOT EXISTS items (name TEXT, price REAL)"
cursor.execute(item_table)

cursor.execute("INSERT INTO items VALUES('beans',19.33)")

connection.commit()
connection.close()
