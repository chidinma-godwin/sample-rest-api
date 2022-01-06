from marshmallow import pre_dump

from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)

    @pre_dump
    def dump_latest_confirmation(self, user):
        user.confirmations = [user.most_recent_confirmation]
        return user
