from utils import db


class Premio(db.Model):
  __tablename__= "premio"

  id = db.Column(db.Integer, primary_key = True)
  id_empresa = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  nome = db.Column(db.String(255))
  descricao = db.Column(db.String(2000))
  pontos = db.Column(db.Integer)

  empresa = db.relationship('Empresa', foreign_keys=id_empresa)


  def __init__(self, id_empresa, nome, descricao, pontos):
    self.id_empresa = id_empresa
    self.nome = nome
    self.descricao = descricao
    self.pontos = pontos