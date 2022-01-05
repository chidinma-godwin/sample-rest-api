from ma import ma

from models.store import StoreModel
from schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.List(ma.Nested(ItemSchema))

    class Meta:
        model = StoreModel
