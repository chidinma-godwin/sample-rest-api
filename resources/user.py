from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    current_user,
    get_jwt,
    get_jwt_identity,
)
from werkzeug.security import safe_str_cmp
from datetime import datetime, timezone


from models.token_block import TokenBlockModel
from messages import (
    DELETED,
    INVALID_CREDENTIALS,
    LOGGED_OUT,
    NO_ADMIN_ACCESS,
    NOT_FOUND,
    REQUIRED_FIELD,
    UNAUTHORISED,
    UNEXPECTED_ERROR,
    USER_ALREADY_EXIST,
    USER_CREATED,
)
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username", type=str, required=True, help=REQUIRED_FIELD.format("username")
)
_user_parser.add_argument(
    "password", type=str, required=True, help=REQUIRED_FIELD.format("password")
)

# TODO: Use bcrypt
class User(Resource):
    @jwt_required()
    def get(self, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user and current_user.id == user_id:
            return user.json()
        return {"msg": UNAUTHORISED}, 401

    @jwt_required()
    def delete(self, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {"msg": DELETED.format("user {user_id}")}
        return {"msg": NOT_FOUND.format("user")}, 404


class UserList(Resource):
    @jwt_required(fresh=True)
    def get(self):
        claims = get_jwt()
        if claims["is_admin"]:
            users = UserModel.find_all()
            return [{"id": user.id, "username": user.username} for user in users]
        return {"msg": NO_ADMIN_ACCESS}


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"msg": USER_ALREADY_EXIST}, 400

        newUser = UserModel(data["username"], data["password"])

        try:
            newUser.save_user()
        except:
            return {"msg": UNEXPECTED_ERROR}, 500

        return {"msg": USER_CREATED}, 201


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        return {"msg": INVALID_CREDENTIALS}, 401


class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        token_block = TokenBlockModel(jti, datetime.now(timezone.utc))
        token_block.save_to_block_list()
        return {"msg": LOGGED_OUT}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(current_user_id, fresh=False)
        return {"access_token": new_token}
