from database import db

class Empresa(db.Model):
  __tablename__= "Empresa"
  id = db.Column(db.Integer, primary_key = True)
  
  cnpj = db.Column(db.String(100))
  nome = db.Column(db.String(100))
  email = db.Column(db.String(100))
  senha = db.Column(db.String(100))

  # +Chaves
  #Vinculos = db.relationship('Vinculo')

  def __init__(self, cnpj, nome, email, senha):
    self.cnpj = cnpj
    self.nome = nome
    self.email = email
    self.senha = senha