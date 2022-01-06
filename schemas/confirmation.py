from sqlalchemy.orm import load_only
from ma import ma

from models.confirmation import ConfirmationModel


class ConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel

        load_only = ("user_id",)
        include_fk = True
