from utils import db
from flask_login import UserMixin

from datetime import datetime, date


class Usuario(db.Model, UserMixin):
  __tablename__ = "usuario"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False, unique=True)
  senha = db.Column(db.String(255), nullable=False)
  telefone = db.Column(db.String(255))
  tipo_usuario = db.Column(db.String(64))

  __mapper_args__ = {'polymorphic_on': tipo_usuario}

  def __init__(self, nome, email, senha, telefone=None):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.telefone = telefone


class Doador(Usuario):
  __mapper_args__ = {'polymorphic_identity': 'Doador'}

  nascimento = db.Column(db.Date)

  def __init__(self, nome, email, senha, nascimento, telefone=None):
    super().__init__(nome, email, senha, telefone)
    self.nascimento = nascimento

class Empresa(Usuario):
  __mapper_args__ = {'polymorphic_identity': 'Empresa'}

  cnpj = db.Column(db.String(14))

  def __init__(self, nome, email, senha, cnpj, telefone=None):
    super().__init__(nome, email, senha, telefone)
    self.cnpj = cnpj


class Administrador(Usuario):
  __mapper_args__ = {'polymorphic_identity': 'Administrador'}

  nivel_acesso = db.Column(db.Integer)

  def __init__(self, nome, email, senha, nivel_acesso=1):
    super().__init__(nome, email, senha)
    self.nivel_acesso = nivel_acesso
