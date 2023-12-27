from flask import Blueprint, url_for, render_template, request, redirect, flash
from utils import db, lm
from flask_login import login_user, logout_user, login_required, current_user

from models.vinculo import Vinculo

bp_vinculo = Blueprint("vinculo", __name__, template_folder="templates")



@bp_vinculo.route('/create', methods=['GET', 'POST'])
def create():

  if request.method=='GET':
    return redirect('/')

  elif request.method=='POST':
    id_doador = request.form.get('id_doador')
    id_empresa = request.form.get('id_empresa')

    vinculo = Vinculo.query.filter_by(id_doador=id_doador, id_empresa=id_empresa).first()
    if vinculo:
      vinculo.status = 'Ativo'
      print('Alterado o estado')
    else:
      vinculo = Vinculo(id_doador, id_empresa)
      
    db.session.add(vinculo) 
    db.session.commit()

    return redirect(url_for('usuario.perfil', id=id_empresa))

@bp_vinculo.route('/desvincular', methods=['GET', 'POST'])
def desvincular():

  if request.method=='GET':
    return redirect('/')

  elif request.method=='POST':
    id_doador = request.form.get('id_doador')
    id_empresa = request.form.get('id_empresa')

    vinculo = Vinculo.query.filter_by(id_doador=id_doador, id_empresa=id_empresa).first()

    if vinculo:
      vinculo.status = "Inativo"
      db.session.add(vinculo) 
      db.session.commit()
      
    return redirect(url_for('usuario.perfil', id=id_empresa))