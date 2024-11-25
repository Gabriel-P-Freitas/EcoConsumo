from flask import Blueprint, url_for, render_template, request, redirect, flash, get_flashed_messages
from utils import db
from flask_login import login_required, current_user

from sqlalchemy import desc
from sqlalchemy.orm import aliased

from models.vinculo import Vinculo
from models.entrega import Entrega
from models.usuario import Doador, Empresa

bp_entrega = Blueprint("entrega", __name__, template_folder="templates")

@bp_entrega.route('/create', defaults={'id_vinculo': None}, methods=['GET', 'POST'])
@bp_entrega.route('/create/<int:id_vinculo>', methods=['GET', 'POST'])
@login_required
def create(id_vinculo):

  if current_user.tipo_usuario not in ['Empresa', 'Administrador']:
    flash('Acesso negado', 'error')
    return redirect('/login')
  
  if not id_vinculo:
    return redirect(url_for('doador.recovery'))

  
  if request.method=='GET':
    return render_template('entrega_create.html', id_vinculo=id_vinculo)

  elif request.method=='POST':
    
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    pontos = request.form.get('pontos')

    ok = 1
    if nome:
      nome = nome.strip()
      if not(len(nome) >= 3):
        flash('Nome deve ter no mínimo 3 caracteres', 'error')      
      else:
        ok += 1
    else:
      flash('Adicione um nome a entrega', 'error')

    if pontos:
      try:
        pontos = int(pontos)
        ok += 1
      except:
        flash('Nome deve ter no mínimo 3 caracteres', 'error')
    else:
      flash('Adicione uma pontuação a entrega', 'error')

    if ok != 3:
      return redirect(request.referrer)
      

    entrega = Entrega(id_vinculo, nome, descricao, pontos)
    vinculo = Vinculo.query.filter_by(id=id_vinculo).first()
    vinculo.pontos += pontos
    
    db.session.add(entrega)     
    db.session.commit()

    flash('Entrega cadastrada com sucesso!', 'success')
    return redirect(url_for('entrega.recovery'))

  return 'Create entrega'


@bp_entrega.route('/recovery', methods=['GET'])
@login_required
def recovery():
  doador_alias = aliased(Doador)
  empresa_alias = aliased(Empresa)

  todas_entregas = db.session.query(
      Entrega, 
      doador_alias, 
      empresa_alias
    ).join(
      Vinculo, 
      Entrega.id_vinculo == Vinculo.id
    ).filter(
      Vinculo.id_doador == doador_alias.id,
      Vinculo.id_empresa == empresa_alias.id
    ).order_by(
      desc(Entrega.data)
    )

  if current_user.tipo_usuario == 'Doador':
    entregas = todas_entregas.filter(Vinculo.id_doador == current_user.id).all()
  elif current_user.tipo_usuario == 'Empresa':
    entregas = todas_entregas.filter(Vinculo.id_empresa == current_user.id).all()
  else:
    entregas = todas_entregas.all()
  
  return render_template('entrega_recovery.html', entregas=entregas)

@bp_entrega.route('/detalhes', defaults={'id_entrega': None}, methods=['GET'])
@bp_entrega.route('/detalhes/<int:id_entrega>', methods=['GET'])
@login_required
def detalhes(id_entrega):
  
  if not id_entrega:
    redirect(url_for('entrega.recovery'))
  
  doador_alias = aliased(Doador)
  empresa_alias = aliased(Empresa)

  todas_entregas = db.session.query(
    Entrega, doador_alias, empresa_alias
    ).join(
      Vinculo, 
      Entrega.id_vinculo == Vinculo.id
    ).filter(
      Vinculo.id_doador == doador_alias.id,
      Vinculo.id_empresa == empresa_alias.id
    ).order_by(
      desc(Entrega.data)
    ).filter(
      Entrega.id == id_entrega
    )

  if current_user.tipo_usuario == 'Doador':
    entregas = todas_entregas.filter(Vinculo.id_doador == current_user.id).all()
  elif current_user.tipo_usuario == 'Empresa':
    entregas = todas_entregas.filter(Vinculo.id_empresa == current_user.id).all()
  else:
    entregas = todas_entregas.all()

  return render_template('entrega_detalhes.html', entregas=entregas)