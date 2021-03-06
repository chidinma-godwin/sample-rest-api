from typing import List
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    price = db.Column(
        db.Float(precision=2),
        nullable=False,
    )
    store_id = db.Column(
        db.Integer,
        db.ForeignKey("stores.id"),
        nullable=False,
    )

    @classmethod
    def find_items(cls) -> List["ItemModel"]:
        return cls.query.all()

    @classmethod
    def find_item(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_item(self) -> None:
        db.session.delete(self)
        db.session.commit()
