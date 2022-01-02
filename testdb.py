import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id INTEGER primary key, username text, password text)"

cursor.execute(create_table)

users=[
        (1, "First user", "password1"),
        (2, "Second user", "password2"),
        (3, "Third user", "password3"),
      ]
insert_query = "INSERT INTO users VALUES (?, ?, ?)"

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for user in cursor.execute(select_query):
  print(user)

connection.commit()
connection.close()
