from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.item import ItemList, Item
from resources.store import Store, StoreList
from resources.user import User, UserRegister, UserLogin, UserList
from models.user import UserModel
import os

app=Flask(__name__)
app.secret_key=os.environ.get("APP_SECRET")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["PROPAGATE_EXCEPTIONS"] = True
api=Api(app)

jwt=JWTManager(app)

@app.before_first_request
def create_tables():
  db.create_all()
  db.session.commit()

@jwt.additional_claims_loader
def add_claims_to_token(identity):
  if identity == 1:
    return {"is_admin": True}
  else:
    return {"is_admin": False}

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).first()

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserList, '/users')



if __name__ == "__main__":
  from db import db
  db.init_app(app)
  app.run(port=5000, debug=True)