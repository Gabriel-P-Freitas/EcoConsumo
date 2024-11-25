from flask import Blueprint, url_for, render_template, request, redirect, flash
from utils import db, lm
from flask_login import login_user, logout_user, login_required, current_user

from models.usuario import Usuario, Administrador

bp_administrador = Blueprint("administrador", __name__, template_folder="templates")


@bp_administrador.route('/create', methods=['GET', 'POST'])
def create():
  if request.method=='GET':
    return redirect('/cadastro')

  elif request.method=='POST':
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    administrador = Administrador(nome, email, senha)
    db.session.add(administrador)
    db.session.commit()

    flash('Administrador cadastrado com sucesso!', 'success')
    return redirect('/login')
  
  return 'Create usuario Administrador'

@bp_administrador.route('/recovery', methods=['GET'])
@login_required
def recovery():
  if current_user.tipo_usuario == 'Administrador':
    administradores = Administrador.query.all()
    return render_template('administrador_recovery.html', administradores=administradores)
  else:
    flash('Acesso negado', 'error')
    return redirect('/login')