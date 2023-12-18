from flask import Blueprint, url_for, render_template, request, redirect, flash
from utils import db, lm
from flask_login import login_user, logout_user, login_required, current_user

import re

from models.usuario import Empresa
from models.vinculo import Vinculo

bp_empresa = Blueprint("empresa", __name__, template_folder="templates")


@bp_empresa.route('/create', methods=['GET', 'POST'])
def create():

  if request.method=='GET':
    return redirect('/cadastro')

  elif request.method=='POST':
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cnpj = request.form.get('cnpj')

    if cnpj:
      cnpj_formatado = re.sub(r'\D', '', cnpj)
    else:
      flash('Informe o CNPJ da empresa', 'error')
      return redirect('/cadastro')

    empresa = Empresa(nome, email, senha, cnpj_formatado)
    db.session.add(empresa) 
    db.session.commit()

    flash('Empresa cadastrada com sucesso!', 'success')
    return redirect('/login')

  return 'Create usuario Empresa'

@bp_empresa.route('/recovery', methods=['GET'])
def recovery():
  todas_empresas = db.session.query(
    Empresa, Vinculo
  ).outerjoin(
    Vinculo, 
    Vinculo.id_empresa==Empresa.id
  )

  if current_user.tipo_usuario == 'Doador':
    empresas = todas_empresas.filter(
      Vinculo.id_doador==current_user.id
    ).all()
  else:
    empresas = todas_empresas.all()
  
  return render_template('empresa_recovery.html', empresas=empresas)