from time import time
import traceback
from flask_restful import Resource
from libs.mailgun import MailgunException

from messages import ALREADY_CONFIRMED, CONFIRMATION_RESENT, NOT_FOUND, UNEXPECTED_ERROR
from models.confirmation import ConfirmationModel
from schemas.confirmation import ConfirmationSchema
from messages import CONFIRMATION_SUCCESSFUL
from models.user import UserModel

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"msg": NOT_FOUND.format("confirmation")}, 400
        if confirmation.confirmed:
            return {"msg": ALREADY_CONFIRMED}, 400
        confirmation.confirmed = True
        confirmation.save_to_db()
        return {"msg": CONFIRMATION_SUCCESSFUL}


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": NOT_FOUND.format("user")}

        conf = UserModel.find_confirmations_by_user(user)
        confirmations = confirmation_schema.dump(
            UserModel.find_confirmations_by_user(user), many=True
        )
        return {"current_time": int(time()), "confirmations": confirmations}

    @classmethod
    def post(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": NOT_FOUND.format("user")}

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"msg": ALREADY_CONFIRMED}, 400

            confirmation.force_to_expire()
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"msg": CONFIRMATION_RESENT}
        except MailgunException as e:
            return {"msg": str(e)}, 500
        except:
            traceback.print_exc()
            return {"msg": UNEXPECTED_ERROR}, 500
