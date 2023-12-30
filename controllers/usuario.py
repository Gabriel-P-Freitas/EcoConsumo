from flask import Blueprint, url_for, render_template, request, redirect, flash
from utils import db, lm
from flask_login import login_user, logout_user, login_required, current_user

from models.usuario import Usuario
from models.usuario import Empresa
from models.usuario import Doador
from models.vinculo import Vinculo

bp_usuario = Blueprint("usuario", __name__, template_folder="templates")


@bp_usuario.route('/perfil', defaults={'id': None}, methods=['GET'])
@bp_usuario.route('/perfil/<int:id>', methods=['GET'])
@login_required
def perfil(id):
  if not id:
    id = current_user.id

  usuario = Usuario.query.filter_by(id=id).first()
  if usuario:
    tipo = usuario.tipo_usuario
  else:
    flash('Usuário não encontrado!', 'success')
    return redirect('/login')

  if tipo == 'Doador':
    if current_user.tipo_usuario == 'Administrador' or current_user.id == id:
      return render_template('perfil.html', user=usuario)
    elif current_user.tipo_usuario == 'Empresa':
      vinculado = False
      vinculo = Vinculo.query.filter_by(id_doador=id, id_empresa=current_user.id).first()
      if vinculo:
        if vinculo.status == 'Ativo':
          vinculado = vinculo.id

        print(f'vinculo: {vinculado}')

        return render_template('perfil.html', user=usuario, vinculado=vinculado)

  elif tipo == 'Empresa':

    if current_user.tipo_usuario == 'Doador':
      vinculado = False
      vinculo = Vinculo.query.filter_by(id_doador=current_user.id, id_empresa=id).first()
      if vinculo:
        if vinculo.status == 'Ativo':
          vinculado = vinculo.id
          
      return render_template('perfil.html', user=usuario, vinculado=vinculado)
    
    return render_template('perfil.html', user=usuario)

  elif tipo == 'Administrador':
    if current_user.tipo_usuario == 'Administrador':
      return render_template('perfil.html', user=usuario)

  flash('Acesso negado', 'error')
  return redirect('/login')



@lm.user_loader
def load_user(id):
  usuario = Usuario.query.filter_by(id=id).first()
  return usuario

@bp_usuario.route('/autenticar', methods=['GET', 'POST'])
def autenticar():

  if request.method=='POST':
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    usuario = Usuario.query.filter_by(email = email).first()

    if usuario:
      if senha == usuario.senha:
        login_user(usuario)
        return redirect(url_for('usuario.perfil'))
      else:
        flash('Senha incorreta', 'error')
    else:
      flash('Email incorreto', 'error')

  return redirect('/login')

@bp_usuario.route('/logout')
def logout():
  logout_user()
  return redirect('/')



## -- ##

@bp_usuario.route('/zautenticar', defaults={'tipo': None}, methods=['GET', 'POST'])
@bp_usuario.route('/zautenticar/<tipo>', methods=['GET', 'POST'])
def zautenticar(tipo):

  tipo = tipo.lower()
  if tipo not in ['doador', 'empresa', 'administrador']:
    redirect(url_for('zselecao'))

  if request.method=='POST':
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if tipo == "doador":
      usuario = Usuario.query.filter_by(email = email).first()
    else:
      usuario = Empresa.query.filter_by(email = email).first()

    if usuario:
      if senha == usuario.senha:
        login_user(usuario)
        return redirect(url_for('usuario.perfil'))
      else:
        flash('Senha incorreta', 'error')
    else:
      flash('Email incorreto', 'error')

  if tipo == 'empresa':
    return redirect(url_for('zlogin_empresa'))
  else:
    return redirect(url_for('zlogin_consumidor'))
