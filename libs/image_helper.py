import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import IMAGES, UploadSet

IMAGE_SET = UploadSet("images", IMAGES)


def save_image(image: FileStorage, filename: str = None, folder: str = None) -> str:
    return IMAGE_SET.save(image, folder, filename)


def get_path(filename: str = None, folder: str = None) -> str:
    return IMAGE_SET.path(filename, folder)


def get_filename(file: Union[FileStorage, str]) -> str:
    if isinstance(file, FileStorage):
        return file.filename
    return file


def get_basename(file: Union[FileStorage, str]) -> str:
    filename = get_filename(file)
    return os.path.split(filename)[1]


def get_file_extension(file: Union[FileStorage, str]) -> str:
    filename = get_filename(file)
    return os.path.splitext(filename)[1]


def is_filename_valid(file: Union[FileStorage, str]):
    filename = get_filename(file)
    allowed_format = "|".join(IMAGES)
    regex = f"^[(a-zA-Z0-9)][a-zA-z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def find_image_any_format(filename: str, folder: str):
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = get_path(image, folder)
        if os.path.isfile(image_path):
            return image_path

    return None
