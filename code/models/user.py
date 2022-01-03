from db import db

class UserModel(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(50))
  password = db.Column(db.Sting(50))

  def __init__(self, username, password):
      self.username = username
      self.password = password

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(name=username).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def save_user(self):
    db.session.add(self)
    db.session.commit()
