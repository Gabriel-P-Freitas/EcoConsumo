from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_migrate import Migrate
from datetime import timedelta

from database import db
from doador import Doador
from empresa import Empresa
from vinculo import Vinculo

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=7)

# --- Banco de dados ORM --- #

app.config['SECRET_KEY'] = 'Jovial Bugle Storage'

conexao = 'mysql+pymysql://psi2023_joel:i]6-sSrG*jGtqDad@albalopes.tech/psi2023_pi_ecoconsumo'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# -------------------------- #

# --- Funções --- #

def to_listOFdict_table(table):
  nao_exibir = ['_sa_instance_state', 'senha']
  
  users = []
  for usuario in table:
    user = {}
    for coluna, valor in vars(usuario).items():
      if coluna not in nao_exibir:
        user[f'{coluna}'] = valor

    users.append(user)

  return users

def to_dict_unique(user):
  dicionario = {}
  for coluna, valor in vars(user).items():
    if coluna not in ['_sa_instance_state', 'senha']:
      dicionario[f'{coluna}'] = valor

  return dicionario

def todos_usuarios():
  doadores = Doador.query.all()
  empresas = Empresa.query.all()
  todos = doadores + empresas

  return todos

def obter_usuario_conectado():
  if 'user' in session:
    tipo = session['user']['tipo']
    id = session['user']['id']

    if tipo == 'doador':
      usuario_conectado = Doador.query.filter_by(id=id).first()
    elif tipo == 'empresa':
      usuario_conectado = Empresa.query.filter_by(id=id).first()
  else:
    usuario_conectado = None
  
  return usuario_conectado

def obter_usuario(tipo, id):
  if tipo == 'doador':
    usuario = Doador.query.filter_by(id=id).first()
  elif tipo == 'empresa':
    usuario = Empresa.query.filter_by(id=id).first()

  return usuario


def obter_tabela_usuario_conectado():
  if 'user' in session:
    tipo = session['user']['tipo']
  
    if tipo == 'doador':
      tabela_conectado = Doador.query.all()
    elif tipo == 'empresa':
      tabela_conectado = Empresa.query.all()
  else:
    tabela_conectado = None
  
  return tabela_conectado

# -------------------------- #

@app.before_request
def check_user_session():
  if 'tema' not in session:
    session['tema'] = 'padrao'
  if request.endpoint not in ['static', 'index', 'login', 'cadastro'] and 'user' not in session:
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    senha = request.form.get('senha')


    doador = Doador.query.filter_by(email=email, senha=senha).first()
    empresa = Empresa.query.filter_by(email=email, senha=senha).first()

    if not (doador or empresa):
      flash('Email ou Senha incorretos.', 'AVISO')
    else:
      if doador:
        user_login = {'tipo': 'doador', 'id': doador.id}
      elif empresa:
        user_login = {'tipo': 'empresa', 'id': empresa.id}

      if 'user' in session and session['user'] == user_login:
        flash('Usuario já conectado.', 'INFO')
      else:
        flash('Login bem sucedido!', 'SUCESSO')
        session.permanent = True
        session['user'] = user_login
      
      return redirect(url_for('perfil'))

  return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():  
  if request.method == 'POST':
    tipo = request.form.get('tipo')
    
    cp = int(request.form.get('cp').replace(".", "").replace("-", ""))
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    
    doador = Doador.query.filter_by(email=email).first()
    empresa = Empresa.query.filter_by(email=email).first()
    if doador or empresa:
      flash('Email já está cadastrado.', 'INFO')
    else:
      if tipo == 'doador':
        obj = Doador(cp, nome, email, senha)
      elif tipo == 'instituicao':
        obj = Empresa(cp, nome, email, senha)
        
      db.session.add(obj)
      db.session.commit()
      flash('Usuario cadastrado com sucesso!', 'SUCESSO')
  
  return render_template('cadastro.html')


@app.route('/buscar')
def buscar():
  tipo = session['user']['tipo']
  

  if tipo == 'doador':
    todos = Empresa.query.all()
    
    nao_exibir = ['_sa_instance_state', 'senha']

    users = []
    for empresa in todos:
      user = {}
      for coluna, valor in vars(empresa).items():
        if coluna not in nao_exibir:
          user[f'{coluna}'] = valor

      vinculo = Vinculo.query.filter_by(id_Empresa=empresa.id, id_Doador=session['user']['id']).first()
      if vinculo:
        user['pontos'] = vinculo.pontos

      users.append(user)

  
  elif tipo == 'empresa':
    todos = Doador.query.all()
    
    nao_exibir = ['_sa_instance_state', 'senha']

    users = []
    for doador in todos:
      user = {}
      for coluna, valor in vars(doador).items():
        if coluna not in nao_exibir:
          user[f'{coluna}'] = valor

      vinculo = Vinculo.query.filter_by(id_Empresa=session['user']['id'], id_Doador=doador.id).first()
      if vinculo:
        user['pontos'] = vinculo.pontos

      users.append(user)

  return render_template('buscar.html', users=users)


@app.route('/perfil', defaults={'tipo': None, 'id': None})
@app.route('/perfil/<tipo>/<id>')
def perfil(tipo, id):
  proprio = False
  if not (tipo or id):
    tipo = session['user']['tipo']
    id = session['user']['id']
    proprio = True
  
  
  usuario = obter_usuario(tipo, id)
  if usuario:
    usuario_dicionario = to_dict_unique(usuario)

  vinculavel = False
  vinculado = False
  if tipo != session['user']['tipo'] and session['user']['tipo'] == 'doador':
    vinculavel = True

    vinculo = Vinculo.query.filter_by(id_Empresa=id, id_Doador=session['user']['id']).first()
    if vinculo:
      vinculado = True
    
  return render_template('perfil.html', usuario=usuario_dicionario, tipo=tipo, proprio=proprio, vinculavel=vinculavel, vinculado=vinculado)

@app.route('/buscaperfil/<id>')
def buscaperfil(id):
  id = int(id)
  tipo_atual = session['user']['tipo']
  if tipo_atual == 'doador':
    tipo = 'empresa'
  elif tipo_atual == 'empresa':
    tipo = 'doador'
    
  return redirect(url_for('perfil', tipo=tipo, id=id))

@app.route('/cmdperfil', methods=['POST'])
def cmdperfil():
  action = request.form.get('action').lower()
  usuario_conectado = obter_usuario_conectado()

  if usuario_conectado:
    if action == 'sair':
      outed = session.pop('user')
    elif action == 'excluir conta':
      db.session.delete(usuario_conectado)
      db.session.commit()
      outed = session.pop('user')

  return redirect(url_for('login'))
  
@app.route('/vincular/<tipo>/<id>', methods=['POST'])
def vincular(tipo, id):

  id_Empresa = id
  id_Doador = session['user']['id']
  
  vinculo = Vinculo.query.filter_by(id_Empresa=id_Empresa , id_Doador=id_Doador).first()
  if vinculo:
    flash('Vinculo já formado.', 'INFO')
  else:
    obj = Vinculo(135, id_Doador, id_Empresa)

    db.session.add(obj)
    db.session.commit()
    flash('Vinculo formado com sucesso!', 'SUCESSO')
  
  return redirect(url_for('perfil', tipo=tipo, id=id))

@app.route('/desvincular/<tipo>/<id>', methods=['POST'])
def desvincular(tipo, id):

  id_Empresa = id
  id_Doador = session['user']['id']

  vinculo = Vinculo.query.filter_by(id_Empresa=id_Empresa , id_Doador=id_Doador).first()
  if vinculo:
    db.session.delete(vinculo)
    db.session.commit()
    flash('Vinculo desfeito.', 'SUCESSO')
  else:
    flash('Ñão há vinculo.', 'INFO')

  return redirect(url_for('perfil', tipo=tipo, id=id))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
