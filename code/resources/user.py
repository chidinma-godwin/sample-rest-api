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

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "INSERT INTO users Values (NULL, ?, ?)"
    cursor.execute(query, (data["username"], data["password"]))

    connection.commit()
    connection.close()

    return {"msg": "User created successfully"}, 201