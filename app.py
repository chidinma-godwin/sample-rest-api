from os import name
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.item import ItemList, Item
from resources.store import Store, StoreList
from resources.user import UserRegister
import os

from security import authenticate, identity

app=Flask(__name__)
app.secret_key=os.environ.get("APP_SECRET")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
api=Api(app)

jwt=JWT(app, authenticate, identity)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<name>')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
  from db import db
  db.init_app(app)
  app.run(port=5000, debug=True)