from typing import Union
from marshmallow import Schema, fields

from schemas.item import ItemSchema


class StoreSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    items = fields.List(fields.Nested(ItemSchema))
