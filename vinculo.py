from database import db

class Vinculo(db.Model):
  __tablename__= "Vinculo"
  id = db.Column(db.Integer, primary_key = True)

  pontos = db.Column(db.Integer)

  # +Chaves
  id_Doador = db.Column(db.Integer, db.ForeignKey('Doador.id', ondelete='CASCADE'))
  #Doador = db.relationship('Doador', foreign_keys=[id])
  
  id_Empresa = db.Column(db.Integer, db.ForeignKey('Empresa.id', ondelete='CASCADE'))
  #Empresa = db.relationship('Empresa', foreign_keys=[id])


  def __init__(self, pontos, id_Doador, id_Empresa):
    self.pontos = pontos
    self.id_Doador = id_Doador
    self.id_Empresa = id_Empresa