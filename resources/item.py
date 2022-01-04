from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt

from models.item import ItemModel

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("price", type=float, required = True)
  parser.add_argument("store_id", type=int, required=True, help="Every item must have a store id")

  @jwt_required(optional=True)
  def get(self, name):
    item = ItemModel.find_item(name)
    if item:
      claims = get_jwt()
      print(claims != {} and claims["is_admin"])
      if claims != {} and claims["is_admin"]:
        return item.json()
      return {"name": item.name, "price": item.price}

    return {"msg": "Item not found"}, 404
  
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
    if items:
      claims = get_jwt()
      if claims["is_admin"]:
        return {"items": [item.json() for item in items]}, 200
      return {"items": [{"name": item.name, "price": item.price} for item in items]}, 200
    return {"msg": "No items found"}, 404
    

