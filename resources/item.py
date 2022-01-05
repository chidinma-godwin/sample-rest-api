from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt

from models.item import ItemModel
from messages import REQUIRED_FIELD, NOT_FOUND, UNEXPECTED_ERROR, DELETED
from schemas.item import ItemSchema

item_schema = ItemSchema()


class Item(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls, name: str):
        item = ItemModel.find_item(name)
        if item:
            claims = get_jwt()
            if claims != {} and claims["is_admin"]:
                return item_schema.dump(item)
            return {"name": item.name, "price": item.price}

        return {"msg": NOT_FOUND.format("item")}, 404

    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()
        item_json["name"] = name
        data = item_schema.load(item_json)
        item = ItemModel.find_item(name)

        if item is None:
            item = ItemModel(**data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item_schema.dump(item)

    @classmethod
    def delete(cls, name: str):
        try:
            item = ItemModel.find_item(name)
            item.delete_item()
        except:
            return {"msg": UNEXPECTED_ERROR}, 500
        return {"msg": DELETED.format("item")}, 200


class ItemList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        items = ItemModel.find_items()
        if items:
            claims = get_jwt()
            if claims["is_admin"]:
                return {"items": item_schema.dump(items, many=True)}, 200
            return {"items": [item_schema.dump(item) for item in items]}, 200
        return {"msg": NOT_FOUND.format("item")}, 404
