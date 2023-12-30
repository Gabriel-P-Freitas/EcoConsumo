from flask import Blueprint, url_for, render_template, request, redirect, flash
from utils import db, lm
from flask_login import login_user, logout_user, login_required, current_user

from models.usuario import Usuario, Doador
from models.vinculo import Vinculo
from datetime import datetime, date

bp_doador = Blueprint("doador", __name__, template_folder="templates")


@bp_doador.route('/create', methods=['GET', 'POST'])
def create():

  if request.method=='GET':
    return redirect('/cadastro')

  elif request.method=='POST':
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    data_nascimento = request.form.get('nascimento')

    if data_nascimento:
      try:
        data_nascimento_formatada = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
      except:
        flash('Data invalida', 'error')
        return redirect('/cadastro')
    else:
      flash('Preencha a data de nascimento', 'error')
      return redirect('/cadastro')
      
    doador = Doador(nome, email, senha, data_nascimento_formatada)
    db.session.add(doador) 
    db.session.commit()
    
    flash('Doador cadastrado com sucesso!', 'success')
    return redirect('/login')

  return 'Create usuario Doador'

@bp_doador.route('/recovery', methods=['GET'])
@login_required
def recovery():
  permitido = False

  if current_user.tipo_usuario == 'Administrador' or current_user.id == id:
    doadores = Doador.query.all()
    return render_template('doador_recovery.html', doadores=doadores)
  elif current_user.tipo_usuario == 'Empresa': # GG
    doadores_vinculados = db.session.query(Doador, Vinculo).filter(Vinculo.id_doador==Doador.id, Vinculo.id_empresa==current_user.id, Vinculo.status == 'Ativo').all()
    #doadores = db.session.query(Doador).join(Vinculo, Vinculo.id_doador==Doador.id).filter(Vinculo.id_empresa==current_user.id, Vinculo.status == 'Ativo').all()

    return render_template('doador_recovery.html', doadores_vinculados=doadores_vinculados)
    
  flash('Acesso negado', 'error')
  return redirect('/login')

@bp_doador.route('/update', methods=['GET'])
@login_required
def update():

  if request.method=='GET':
    return render_template('update_recovery.html')

  if request.method=='POST':
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')
    cpf = request.form.get('cpf')
    idade = request.form.get('idade')

    doador = Doador.query.filter_by(id=id).first()

    if doador:
      doador.nome = nome
      doador.email = email
      doador.senha = senha
      doador.telefone = telefone
      doador.cpf = cpf
      doador.idade = idade

      db.session.add(doador)
      db.session.commit()
        
    return render_template('index.html')

  return 'Recovery usuario Doador'



## -- ##

@bp_doador.route('/zcreate', methods=['GET', 'POST'])
def zcreate():

  if request.method=='GET':
    return redirect(url_for('zcadastro_consumidor'))

  elif request.method=='POST':
    nome = request.form.get('nome')
    data_nascimento = request.form.get('nascimento').replace('-', '/')
    telefone = request.form.get('telefone')

    email = request.form.get('email')
    senha = request.form.get('senha')
    confirmar = request.form.get('confirmar')

    erro = 0
    if data_nascimento:
      try:
        data_nascimento_formatada = datetime.strptime(data_nascimento, '%Y/%m/%d').date()
      except:
        flash('Data invalida', 'error')
        return redirect(url_for('zcadastro_consumidor'))
    else:
      flash('Preencha a data de nascimento', 'error')
      return redirect(url_for('zcadastro_consumidor'))

    if not nome:
      flash('Digite o nome', 'error')
      erro += 1

    if not email:
      flash('Digite o email', 'error')
      erro += 1
    
    if not senha:
      flash('Digite a senha', 'error')
      erro += 1

    if not telefone:
      flash('Digite o telefone', 'error')
      erro += 1

    if erro != 0:
      return redirect(url_for('zcadastro_consumidor'))


    usuario = Usuario.query.filter_by(email = email).first()

    if not usuario:
      doador = Doador(nome, email, senha, data_nascimento_formatada, telefone)
      db.session.add(doador) 
      db.session.commit()
      
      flash('Doador cadastrado com sucesso!', 'success')
      return redirect(url_for('zlogin_consumidor'))
    else:
      flash('Já existe um usuario com esse email', 'error')
      return redirect(url_for('zcadastro_consumidor'))

  return 'Create usuario Doador'