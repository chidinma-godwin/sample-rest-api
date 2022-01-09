import os

DEBUG = True
SECRET_KEY = os.environ["SECRET_KEY"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
