from flask_restful import Resource, reqparse
import sqlite3

from models.user import UserModel

class UserRegister(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("username", type=str, required = True)
  parser.add_argument("password", type=str, required = True)

  def post(self):
    data = UserRegister.parser.parse_args()

    if UserModel.find_by_username(data["username"]):
      return {"msg": "Username already exists"}, 400

    newUser = UserModel(data["username"], data["password"])

    try:
      newUser.save_user()
    except:
      return {"msg": "Unexpected error"}, 500

    return {"msg": "User created successfully"}, 201