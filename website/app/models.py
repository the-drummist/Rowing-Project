from . import db
from datetime import datetime

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  username = db.Column(db.String(80), nullable=False, unique=True)
  email = db.Column(db.String(320), nullable=False, unique=True)
  hash = db.Column(db.String(92), nullable=False)
  birthday = db.Column(db.Date, nullable=True)
  weight = db.Column(db.Integer, nullable=True)
  sex = db.column(db.String(6), nullable=True)
  rhr = db.Column(db.Integer, nullable=True)
  upload_id = db.Column(db.Integer, nullable=False, unique=True)

  #def __repr__(self):
  #  return "<User {}".format(self.id)
