import os
from typing import List
from flask import request, url_for
from requests import Response, post

from db import db
from libs.mailgun import Mailgun
from models.confirmation import ConfirmationModel


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    confirmations = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    def save_user(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @property
    def most_recent_confirmation(self):
        return self.confirmations.order_by(
            db.desc(ConfirmationModel.expired_at)
        ).first()

    @classmethod
    def find_confirmations_by_user(cls, user: "UserModel"):
        return user.confirmations.order_by(db.desc(ConfirmationModel.expired_at)).all()

    def send_confirmation_email(self) -> Response:
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=self.most_recent_confirmation.id
        )
        MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
        MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
        return Mailgun.send_email(
            email=[
                self.email,
            ],
            subject="Registration Confirmation",
            text=f"Please click the link below to confirm your account. {link}",
            html=f'<html>Please click <a href="{link}">{link}</a> to confirm your account.</html>',
        )
