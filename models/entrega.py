from utils import db
from datetime import datetime


class Entrega(db.Model):
  __tablename__= "entrega"

  id = db.Column(db.Integer, primary_key = True)
  id_vinculo = db.Column(db.Integer, db.ForeignKey('vinculo.id'))
  nome = db.Column(db.String(255))
  descricao = db.Column(db.String(2000))
  pontos = db.Column(db.Integer)
  data = db.Column(db.Date)

  vinculo = db.relationship('Vinculo', foreign_keys=id_vinculo)


  def __init__(self, id_vinculo, nome, descricao, pontos):
    self.id_vinculo = id_vinculo
    self.nome = nome
    self.descricao = descricao
    self.pontos = pontos

    self.data = datetime.today()