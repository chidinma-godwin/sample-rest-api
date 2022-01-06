import traceback
from flask_restful import Resource
from flask import request
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
from libs.mailgun import MailgunException
from models.confirmation import ConfirmationModel


from models.token_block import TokenBlockModel
from messages import (
    DELETED,
    INVALID_CREDENTIALS,
    LOGGED_OUT,
    NO_ADMIN_ACCESS,
    NOT_ACTIVATED,
    NOT_FOUND,
    REGISTRATION_FAILED,
    UNAUTHORISED,
    UNEXPECTED_ERROR,
    USER_ALREADY_EXIST,
    USER_CREATED,
    EMAIL_ALREADY_USED,
)
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()

# TODO: Use bcrypt
class User(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user and current_user.id == user_id:
            return user_schema.dump(user)
        return {"msg": UNAUTHORISED}, 401

    @classmethod
    @jwt_required()
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {"msg": DELETED.format(f"user {user_id}")}
        return {"msg": NOT_FOUND.format("user")}, 404


class UserList(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls):
        claims = get_jwt()
        if claims["is_admin"]:
            users = UserModel.find_all()
            return user_schema.dump(users, many=True)
        return {"msg": NO_ADMIN_ACCESS}


class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = user_schema.load(request.get_json())

        if UserModel.find_by_username(data["username"]):
            return {"msg": USER_ALREADY_EXIST}, 400

        if UserModel.find_by_email(data["email"]):
            return {"msg": EMAIL_ALREADY_USED}, 400

        newUser = UserModel(**data)

        try:
            newUser.save_user()
            confirmation = ConfirmationModel(newUser.id)
            confirmation.save_to_db()
            newUser.send_confirmation_email()
        except MailgunException as e:
            newUser.delete_from_db()
            return {"msg": REGISTRATION_FAILED}
        except:
            traceback.print_exc()
            newUser.delete_from_db()
            return {"msg": UNEXPECTED_ERROR}, 500

        return {"msg": USER_CREATED}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = user_schema.load(request.get_json(), partial=("email",))
        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
            return {"msg": NOT_ACTIVATED}, 401

        return {"msg": INVALID_CREDENTIALS}, 401


class Logout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        token_block = TokenBlockModel(jti, datetime.now(timezone.utc))
        token_block.save_to_block_list()
        return {"msg": LOGGED_OUT}


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(current_user_id, fresh=False)
        return {"access_token": new_token}
