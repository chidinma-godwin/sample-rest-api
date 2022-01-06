import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from resources.item import ItemList, Item
from resources.store import Store, StoreList
from resources.user import (
    Logout,
    TokenRefresh,
    User,
    UserRegister,
    UserLogin,
    UserList,
)
from resources.confirmation import ConfirmationByUser, Confirmation
from models.token_block import TokenBlockModel
from models.user import UserModel
from messages import TOKEN_REVOKED_ERR, TOKEN_REVOKED_MSG
from ma import ma

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["PROPAGATE_EXCEPTIONS"] = True
api = Api(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation_error(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_token(identity):
    if os.environ.get("ADMIN_ID") == str(identity):
        return {"is_admin": True}
    else:
        return {"is_admin": False}


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).first()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    token = TokenBlockModel.find_by_jti(jwt_payload["jti"])
    if token:
        return True


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": TOKEN_REVOKED_MSG, "err": TOKEN_REVOKED_ERR})


api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserList, "/users")
api.add_resource(TokenRefresh, "/refresh-token")
api.add_resource(Logout, "/logout")
api.add_resource(Confirmation, "/user-confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/<int:user_id>")


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    ma.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
        db.session.commit()

    app.run(port=5000, debug=True)
