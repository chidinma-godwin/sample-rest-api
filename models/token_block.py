from datetime import datetime

from db import db

class TokenBlockModel(db.Model):
    __tablename__ = "blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique = True)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti: str, created_at: datetime) -> None:
        self.jti = jti
        self.created_at = created_at

    @classmethod
    def find_by_jti(cls, jti: str) -> 'TokenBlockModel':
      return cls.query.filter_by(jti=jti).first()

    def save_to_block_list(self) -> None:
      db.session.add(self)
      db.session.commit()