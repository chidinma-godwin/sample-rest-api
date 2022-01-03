from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class ItemList(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("price", type=float, required = True)

  @jwt_required()
  def get(self, name):
    item = ItemModel.find_item(name)
    return item.json()
  
  def put(self, name):
    data = ItemList.parser.parse_args()
    item = ItemModel.find_item(name)

    if item is None:
      item = ItemModel(name, data["price"])
    else:
      item.price = data["price"]
    item.save_to_db()
    return item.json()

  def delete(self, name):
    try:
      item = ItemModel.find_item(name)
      item.delete_item()
    except Exception as e:
      return { "msg": f"Unexpected error - {e}"}, 500
    return {"msg": "Item deleted"}, 200



class Items(Resource):
   @jwt_required()
   def get(self):
    items = ItemModel.find_items()
    print(items)
    if items:
      return {"items": [item.json() for item in items]}, 200
    return {"msg": "No items found"}, 404
    

