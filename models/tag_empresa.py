from utils import db


class TagEmpresa(db.Model):
  __tablename__= "tag_empresa"

  id = db.Column(db.Integer, primary_key = True)
  id_empresa = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  id_tag = db.Column(db.Integer, db.ForeignKey('tag.id'))

  empresa = db.relationship('Empresa', foreign_keys=id_empresa)
  doador = db.relationship('Tag', foreign_keys=id_tag)


  def __init__(self, id_empresa, id_tag):
    self.id_empresa = id_empresa
    self.id_tag = id_tag