import os
from typing import List
from requests import Response, post

from messages import (
    MAILGUN_API_LOADING_FAILED,
    MAILGUN_DOMAIN_LOADING_FAILED,
    SENDING_CONFIRMATION_FAILED,
)


class MailgunException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Mailgun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException(MAILGUN_API_LOADING_FAILED)
        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException(MAILGUN_DOMAIN_LOADING_FAILED)

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"Store Rest API <mailgun@{cls.MAILGUN_DOMAIN}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            raise MailgunException(SENDING_CONFIRMATION_FAILED)
