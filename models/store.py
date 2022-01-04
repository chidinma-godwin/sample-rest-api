from db import db

class StoreModel(db.Model):
  __tablename__ = "stores"

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(60), unique = True)
  items = db.relationship("ItemModel", backref="store", lazy="dynamic")

  def __init__(self, name):
      self.name = name

  @classmethod
  def find_stores(cls):
    return cls.query.all()

  @classmethod
  def find_store(cls, name):
    return cls.query.filter_by(name=name).first()

  def json(self):
    return {"name": self.name, "items": [item.json() for item in self.items.all()]}

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_store(self):
    db.session.delete(self)
    db.session.commit()