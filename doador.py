from database import db

class Doador(db.Model):
  __tablename__= "Doador"
  id = db.Column(db.Integer, primary_key = True)
  
  cpf = db.Column(db.String(100))
  nome = db.Column(db.String(100))
  email = db.Column(db.String(100))
  senha = db.Column(db.String(100))

  # +Chaves
  #Vinculos = db.relationship('Vinculo')

  def __init__(self, cpf, nome, email, senha):
    self.cpf = cpf
    self.nome = nome
    self.email = email
    self.senha = senha