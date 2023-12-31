from flask import Blueprint, url_for, render_template, request, redirect, flash
from utils import db, lm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_, desc

import re

from models.usuario import Usuario, Empresa
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
    Empresa, 
    Vinculo
  ).outerjoin(
    Vinculo, 
    Vinculo.id_empresa==Empresa.id,
  )

  
  if current_user.tipo_usuario == 'Doador':
    empresas = todas_empresas.filter(
      or_(
        Vinculo.id_doador == current_user.id,
        Vinculo.id_doador.is_(None)
      )
    ).order_by(
      desc(Vinculo.id_doador.isnot(None))
    ).all()
  else:
    empresas = todas_empresas.all()
  
  return render_template('empresa_recovery.html', empresas=empresas)



## -- ##

@bp_empresa.route('/zcreate', methods=['GET', 'POST'])
def zcreate():

  if request.method=='GET':
    return redirect(url_for('zcadastro_empresa'))

  elif request.method=='POST':
    nome = request.form.get('nome').strip()
    cnpj = request.form.get('cnpj').strip()
    telefone = request.form.get('telefone').strip()

    email = request.form.get('email').strip()
    senha = request.form.get('senha').strip()
    confirmar = request.form.get('confirmar').strip()

    erro = 0
    if not nome:
      flash('Nome invalido', 'error')
      erro += 1

    if not cnpj:
      flash('CNPJ invalido', 'error')
      erro += 1

    if not telefone:
      flash('Telefone invalido', 'error')
      erro += 1

    if not email:
      flash('Email invalida', 'error')
      erro += 1

    if not senha:
      flash('Senha invalida', 'error')
      erro += 1

    if senha != confirmar:
      flash('As senhas não correspondem', 'error')
      erro += 1
      
    if erro != 0:
      return redirect(url_for('zcadastro_empresa'))


    usuario = Usuario.query.filter_by(email = email).first()

    if not usuario:
      empresa = Empresa(nome, email, senha, cnpj, telefone)
      db.session.add(empresa) 
      db.session.commit()
      
      flash('Empresa cadastrado com sucesso!', 'success')
      return redirect(url_for('zlogin_empresa'))
    else:
      flash('Já existe um usuario com esse email', 'error')
      return redirect(url_for('zcadastro_consumidor'))

  return 'Create usuario Empresa'