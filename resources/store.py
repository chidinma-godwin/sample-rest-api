from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name: str):
        store = StoreModel.find_store(name)
        return store.json()

    def post(self, name: str):
        store = StoreModel.find_store(name)

        if store is None:
            store = StoreModel(name)
        else:
            store.name = name
        store.save_to_db()
        return store.json()

    def delete(self, name: str):
        try:
            store = StoreModel.find_store(name)
            store.delete_store()
        except:
            return {"msg": "Unexpected error"}, 500
        return {"msg": "store deleted"}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        stores = StoreModel.find_stores()
        if stores:
            return {"stores": [store.json() for store in stores]}
        return {"msg": "No stores found"}, 404
