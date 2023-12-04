from utils import db


class Tag(db.Model):
  __tablename__= "tag"

  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(255))

  def __init__(self, nome):
    self.nome = nome