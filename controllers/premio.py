from flask import Blueprint, url_for, render_template, request, redirect, flash, get_flashed_messages
from utils import db
from flask_login import login_required, current_user

from sqlalchemy import desc
from sqlalchemy.orm import aliased

from models.vinculo import Vinculo
from models.premio import Premio
from models.premio_resgatado import PremioResgatado
from models.usuario import Doador, Empresa

bp_premio = Blueprint("premio", __name__, template_folder="templates")

@bp_premio.route('/create', methods=['GET', 'POST'])
@login_required
def create():

  if current_user.tipo_usuario not in ['Empresa']:
    flash('Acesso negado', 'error')
    return redirect('/login')

  if request.method=='GET':
    return render_template('premio_create.html')

  elif request.method=='POST':

    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    pontos = request.form.get('pontos')

    ok = 0
    if nome:
      nome = nome.strip()
      if not(len(nome) >= 3):
        flash('Nome deve ter no mínimo 3 caracteres', 'error')      
      else:
        ok += 1
    else:
      flash('Adicione um nome a premio', 'error')

    if descricao:
      descricao = descricao.strip()
      if not(len(descricao) >= 10):
        flash('Descrição deve ter no mínimo 10 caracteres', 'error')      
      else:
        ok += 1
    else:
      flash('Adicione uma decrição ao premio', 'error')

    if pontos:
      try:
        pontos = int(pontos)
        ok += 1
      except:
        flash('Nome deve ter no mínimo 3 caracteres', 'error')
    else:
      flash('Adicione uma pontuação ao premio', 'error')

    if ok != 3:
      return redirect(request.url)

    id_empresa = current_user.id
    premio = Premio(id_empresa, nome, descricao, pontos)
    db.session.add(premio)     
    db.session.commit()

    flash('Premio cadastrada com sucesso!', 'success')
    return redirect(url_for('premio.recovery'))

  return 'Create premio'


@bp_premio.route('/recovery', methods=['GET'])
@login_required
def recovery():
  
  todos_premios = db.session.query(
      Premio
    ).order_by(
      Premio.pontos
    )

  if current_user.tipo_usuario == 'Empresa':
    premios = todos_premios.join(Empresa, Premio.id_empresa == current_user.id).all()
  else:
    premios = todos_premios.all()

  return render_template('premio_recovery.html', premios=premios)


@bp_premio.route('/detalhes', defaults={'id_premio': None}, methods=['GET'])
@bp_premio.route('/detalhes/<int:id_premio>', methods=['GET'])
@login_required
def detalhes(id_premio):
  
  if not id_premio:
    return redirect(url_for('premio.recovery'))
    
  todos_premios = db.session.query(
    Premio, 
    Empresa
  ).filter(
    Empresa.id==Premio.id_empresa, 
    Premio.id==id_premio
  )
  
  premios = todos_premios.all()
  if not premios:
    return redirect(url_for('premio.recovery'))

  return render_template('premio_detalhes.html', premios=premios)


@bp_premio.route('/solicitar_resgate', defaults={'id_premio': None}, methods=['GET'])
@bp_premio.route('/solicitar_resgate/<int:id_premio>', methods=['GET'])
@login_required
def solicitar_resgate(id_premio):
  
  if not id_premio:
    return redirect(url_for('premio.recovery'))
  id_doador = current_user.id

  premio =  db.session.query(Premio).filter(Premio.id==id_premio).first()

  vinculo = db.session.query(
    Vinculo
  ).filter(
    Vinculo.id_doador==id_doador,
    Vinculo.id_empresa==premio.id_empresa
  ).first()

  if not vinculo:
    flash('Crie um vinculo com a empresa primeiro.', 'error')  
    return redirect(url_for('usuario.perfil', id=premio.id_empresa))
    
  if not(vinculo.pontos > premio.pontos):
    flash(f'Você não tem pontos suficientes para resgatar esse premio.  Meus pontos: {vinculo.pontos}', 'error')
    return redirect(url_for('premio.recovery'))
    
  vinculo.pontos -= premio.pontos
  premioR = PremioResgatado(id_doador, id_premio)
  db.session.add(premioR)  
  db.session.commit()
  
  flash(f'Você resgatou o premio {premio.nome} com sucesso.', 'success')
  return redirect(url_for('premio.recovery'))


@bp_premio.route('/solicitados_recovery', methods=['GET'])
@login_required
def solicitados_recovery():

  doador_alias = aliased(Doador)
  empresa_alias = aliased(Empresa)
  
  todos_premiosR = db.session.query(
    PremioResgatado, Premio, empresa_alias, doador_alias
  ).filter(
    PremioResgatado.id_premio == Premio.id,
    PremioResgatado.id_doador == doador_alias.id,
    Premio.id_empresa == empresa_alias.id
  )
  
  if current_user.tipo_usuario == 'Empresa':
    premiosR = todos_premiosR.filter(
      empresa_alias.id == current_user.id
    ).all()
  elif current_user.tipo_usuario == 'Doador':
    premiosR = todos_premiosR.filter(
      doador_alias.id == current_user.id
    ).all()
  elif currenet_user.tipo_usuario == 'Administrador':
    premiosR = todos_premiosR.all()
  
  return render_template('premio_solicitado_recovery.html', premiosR=premiosR)

@bp_premio.route('/solicitado_resultado/<int:id_resgate>', methods=['POST'])
@login_required
def solicitado_resultado(id_resgate):  
  
  decisao = request.form.get('status')

  premioR = db.session.query(
    PremioResgatado
  ).filter(
    PremioResgatado.id == id_resgate
  ).first()

  if not premioR or premioR.status in ['aceito', 'recusado']:
    flash(f'Já foi resgatado ou recusado.', 'error')
  else:
    if decisao == 'aceito':
      premioR.status = 'aceito'
      
    elif decisao == 'recusado':
      premioR.status = 'recusado'

      premio = db.session.query(
        Premio
      ).join(
        PremioResgatado,
        PremioResgatado.id_premio == Premio.id
      ).filter(
        PremioResgatado.id == id_resgate
      ).first()
      
      vinculo_doador = db.session.query(
        Vinculo
      ).join(
        PremioResgatado,
        PremioResgatado.id == id_resgate
      ).join(
        Premio,
        Premio.id == PremioResgatado.id_premio
      ).filter(
        Vinculo.id_doador == PremioResgatado.id_doador,
        Vinculo.id_empresa == Premio.id_empresa
      ).first()

      vinculo_doador.pontos += premio.pontos
    
    db.session.commit()
    flash(f'A solicitação foi {decisao.lower()[:-1]}a.', 'success')
  
  return redirect(url_for('premio.solicitados_recovery'))