from typing import List
from uuid import uuid4
from time import time

from db import db

CONFIRMATION_EXPIRATION_DELTA = 1800


class ConfirmationModel(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    expired_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, user_id=int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = uuid4().hex
        self.user_id = user_id
        self.expired_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA

    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    @property
    def expired(self) -> bool:
        return time() > self.expired_at

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def force_to_expire(self) -> None:
        if not self.expired:
            self.expired_at = int(time())
            self.save_to_db()
