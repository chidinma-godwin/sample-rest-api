from typing import List

from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    items = db.relationship("ItemModel", backref="store", lazy="dynamic")

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def find_stores(cls) -> List["StoreModel"]:
        return cls.query.all()

    @classmethod
    def find_store(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_store(self) -> None:
        db.session.delete(self)
        db.session.commit()
