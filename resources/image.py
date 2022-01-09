import os
import traceback
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, send_file

from schemas.image import ImageSchema
from libs import image_helper
from messages import (
    DELETED,
    IMAGE_UPLOAD_SUCCESSFL,
    IMAGE_UPLOAD_FAILED,
    NOT_FOUND,
    UNEXPECTED_ERROR,
    IMAGE_DELETE_FAILED,
)

image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required()
    def post(self):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            print(basename)
            return {"msg": IMAGE_UPLOAD_SUCCESSFL.format(basename)}
        except Exception as e:
            print(e)
            extension = image_helper.get_file_extension(data["image"])
            return {"msg": IMAGE_UPLOAD_FAILED.format(extension)}


class Image(Resource):
    @jwt_required()
    def get(self, filename):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_helper.is_filename_valid(filename):
            return {"msg": NOT_FOUND.format(filename)}
        try:
            image_path = image_helper.get_path(filename, folder)
            return send_file(image_path)
        except FileNotFoundError:
            return {"msg": NOT_FOUND.format(filename)}
        except:
            return {"msg": UNEXPECTED_ERROR}

    @jwt_required()
    def delete(self, filename):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_helper.is_filename_valid(filename):
            return {"msg": NOT_FOUND.format(filename)}
        try:
            os.remove(image_helper.get_path(filename, folder))
            return {"msg": DELETED.format(filename)}
        except FileNotFoundError:
            return {"msg": NOT_FOUND.format(filename)}
        except:
            traceback.print_exc()
            return {"msg": IMAGE_DELETE_FAILED.format(filename)}
