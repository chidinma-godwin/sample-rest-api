from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
