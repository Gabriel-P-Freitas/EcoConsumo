from utils import db


class PremioResgatado(db.Model):
  __tablename__= "premio_resgatado"

  id = db.Column(db.Integer, primary_key = True)
  id_doador = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  id_premio = db.Column(db.Integer, db.ForeignKey('premio.id'))
  status = db.Column(db.String(64)) # Concedido, Cancelado, Em Andamento

  doador = db.relationship('Doador', foreign_keys=id_doador)
  premio = db.relationship('Premio', foreign_keys=id_premio)


  def __init__(self, id_doador, id_premio):
    self.id_doador = id_doador
    self.id_premio = id_premio

    self.status = "Em Andamento"