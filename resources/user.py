from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.user import UserModel

class User(Resource):
  @jwt_required()
  def get(self, user_id):
    user = UserModel.find_by_id(user_id)
    if user:
      return user.json()
    return {"msg": "User not found"}, 404

  @jwt_required()
  def delete(self, user_id):
    user = UserModel.find_by_id(user_id)
    if user:
      user.delete_from_db()
      return {"msg": "User deleted"}
    return {"msg": "User not found"}, 404
    


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
    