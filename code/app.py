from os import name
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.item import Items, ItemList
from resources.user import UserRegister

from security import authenticate, identity

app=Flask(__name__)
app.secret_key='95e49e9410af9ed8ca6854a148c1761d'
api=Api(app)
jwt=JWT(app, authenticate, identity)

api.add_resource(Items, '/items')
api.add_resource(ItemList, '/item/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
  app.run(port=5000, debug=True)