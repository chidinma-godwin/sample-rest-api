from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.store import StoreModel
from messages import DELETED, NOT_FOUND, UNEXPECTED_ERROR


class Store(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        store = StoreModel.find_store(name)
        return store.json()

    @classmethod
    def post(cls, name: str):
        store = StoreModel.find_store(name)

        if store is None:
            store = StoreModel(name)
        else:
            store.name = name
        store.save_to_db()
        return store.json()

    @classmethod
    def delete(cls, name: str):
        try:
            store = StoreModel.find_store(name)
            store.delete_store()
        except:
            return {"msg": UNEXPECTED_ERROR}, 500
        return {"msg": DELETED.format(name)}


class StoreList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        stores = StoreModel.find_stores()
        if stores:
            return {"stores": [store.json() for store in stores]}
        return {"msg": NOT_FOUND.format("store")}, 404
