from utils import db
from datetime import datetime


class Vinculo(db.Model):
  __tablename__ = "vinculo"

  id = db.Column(db.Integer, primary_key=True)
  id_doador = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  id_empresa = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  pontos = db.Column(db.Integer)
  data = db.Column(db.Date)
  status = db.Column(db.String(64))  # Ativo, Inativo

  doador = db.relationship('Doador', foreign_keys=id_doador)
  empresa = db.relationship('Empresa', foreign_keys=id_empresa)

  def __init__(self, id_doador, id_empresa, pontos=0):
    self.id_doador = id_doador
    self.id_empresa = id_empresa
    self.pontos = pontos

    self.data = datetime.today()
    self.status = 'Ativo'
