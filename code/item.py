import sqlite3

from flask_restful import Resource, reqparse

class ItemList(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("price", type=float, required = True)

  @classmethod
  def find_item(cls, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM items WHERE name=?"
    result = cursor.execute(query, (name,))
    row = result.fetchone()
    connection.close()

    if row:
      return {"name": row[0], "price": row[1]}

  @classmethod
  def insert(cls, item):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "INSERT INTO items VALUES (?, ?)"
    cursor.execute(query, (item["name"], item["price"]))
    connection.commit()
    connection.close()

  @classmethod
  def update(cls, item):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "UPDATE items SET price=? WHERE name=?"
    cursor.execute(query, (item["price"], item["name"]))
    connection.commit()
    connection.close()

  @classmethod
  def delete_item(cls, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "DELETE FROM items WHERE name=?"
    cursor.execute(query, (name,))
    connection.commit()
    connection.close()

  def get(self, name):
    item = self.find_item(name)
    return item
  
  def put(self, name):
    data = ItemList.parser.parse_args()
    item = self.find_item(name)

    updatedItem = {"name": name, "price": data["price"]}

    if item:
      try:
        self.update(updatedItem)
      except:
        return {"msg": "Unexpected error"}, 500
    else:
      self.insert(updatedItem)
    return updatedItem

  def delete(self, name):
    try:
      self.delete_item(name)
    except:
      return { "msg": "Unexpected error"}, 500
    return {"msg": "Item deleted"}, 200



class Items(Resource):
  @classmethod
  def find_items(cls):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM items"
    result = cursor.execute(query)
    row = result.fetchall()
    connection.close()

    if row:
      return [{"name": item[0], "price": item[1]} for item in row]

  def get(self):
    items = self.find_items()
    if items:
      return {"items": items}, 200
    return {"msg": "No items found"}, 404
    

