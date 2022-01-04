from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt

from models.item import ItemModel
from messages import REQUIRED_FIELD, NOT_FOUND, UNEXPECTED_ERROR, DELETED


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=REQUIRED_FIELD.format("price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=REQUIRED_FIELD.format("store_id")
    )

    @jwt_required(optional=True)
    def get(self, name: str):
        item = ItemModel.find_item(name)
        if item:
            claims = get_jwt()
            if claims != {} and claims["is_admin"]:
                return item.json()
            return {"name": item.name, "price": item.price}

        return {"msg": NOT_FOUND.format("item")}, 404

    def put(self, name: str):
        data = Item.parser.parse_args()
        item = ItemModel.find_item(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json()

    def delete(self, name: str):
        try:
            item = ItemModel.find_item(name)
            item.delete_item()
        except:
            return {"msg": UNEXPECTED_ERROR}, 500
        return {"msg": DELETED.format("item")}, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.find_items()
        if items:
            claims = get_jwt()
            if claims["is_admin"]:
                return {"items": [item.json() for item in items]}, 200
            return {
                "items": [{"name": item.name, "price": item.price} for item in items]
            }, 200
        return {"msg": NOT_FOUND.format("item")}, 404
