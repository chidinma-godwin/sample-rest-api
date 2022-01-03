from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("price", type=float, required = True)
  parser.add_argument("store_id", type=int, required=True, help="Every item must have a store id")

  @jwt_required()
  def get(self, name):
    item = ItemModel.find_item(name)
    return item.json()
  
  def put(self, name):
    data = Item.parser.parse_args()
    item = ItemModel.find_item(name)

    if item is None:
      item = ItemModel(name, **data)
    else:
      item.price = data["price"]
      item.store_id = data["store_id"]
    item.save_to_db()
    return item.json()

  def delete(self, name):
    try:
      item = ItemModel.find_item(name)
      item.delete_item()
    except Exception as e:
      return { "msg": f"Unexpected error - {e}"}, 500
    return {"msg": "Item deleted"}, 200



class ItemList(Resource):
   @jwt_required()
   def get(self):
    items = ItemModel.find_items()
    print(items)
    if items:
      return {"items": [item.json() for item in items]}, 200
    return {"msg": "No items found"}, 404
    

