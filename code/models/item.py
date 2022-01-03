import sqlite3

class ItemModel:
  def __init__(self, name, price):
      self.name = name
      self.price = price

  @classmethod
  def find_items(cls):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM items"
    result = cursor.execute(query)
    rows = result.fetchall()
    connection.close()

    if rows:
      return [cls(row[0], row[1]) for row in rows]

  @classmethod
  def find_item(cls, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM items WHERE name=?"
    result = cursor.execute(query, (name,))
    row = result.fetchone()
    connection.close()

    if row:
      return cls(*row)

  def json(self):
    return {"name": self.name, "price": self.price}

  def insert(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "INSERT INTO items VALUES (?, ?)"
    cursor.execute(query, (self.name, self.price))
    connection.commit()
    connection.close()

  def update(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "UPDATE items SET price=? WHERE name=?"
    cursor.execute(query, (self.price, self.name))
    connection.commit()
    connection.close()

  def delete_item(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "DELETE FROM items WHERE name=?"
    cursor.execute(query, (self.name,))
    connection.commit()
    connection.close()
