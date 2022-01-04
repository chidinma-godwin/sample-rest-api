from db import db

class ItemModel(db.Model):
  __tablename__ = "items"

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(60))
  price = db.Column(db.Float(precision = 2))
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

  def __init__(self, name, price, store_id):
      self.name = name
      self.price = price
      self.store_id =store_id

  @classmethod
  def find_items(cls):
    return cls.query.all()

  @classmethod
  def find_item(cls, name):
    return cls.query.filter_by(name=name).first()

  def json(self):
    return {"name": self.name, "price": self.price, "store_id": self.store_id}

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_item(self):
    db.session.delete(self)
    db.session.commit()