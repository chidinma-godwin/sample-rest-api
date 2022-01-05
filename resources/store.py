from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.store import StoreModel
from messages import DELETED, NOT_FOUND, UNEXPECTED_ERROR
from schemas.store import StoreSchema

store_schema = StoreSchema()


class Store(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        store = StoreModel.find_store(name)
        return store_schema.dump(store)

    @classmethod
    def post(cls, name: str):
        store = StoreModel.find_store(name)

        if store is None:
            store = StoreModel(name=name)
        else:
            store.name = name
        store.save_to_db()
        return store_schema.dump(store)

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
            return {"stores": store_schema.dump(stores, many=True)}
        return {"msg": NOT_FOUND.format("store")}, 404
