from flask import Flask, render_template, request, redirect, url_for, flash
from utils import db, lm
from flask_migrate import Migrate

from controllers.usuario import bp_usuario
from controllers.doador import bp_doador
from controllers.empresa import bp_empresa
from controllers.administrador import bp_administrador
from controllers.vinculo import bp_vinculo
from controllers.entrega import bp_entrega
from controllers.premio import bp_premio

# -------------------------- #

app = Flask(__name__)

conexao = 'mysql+pymysql://psi2023_joel:i]6-sSrG*jGtqDad@albalopes.tech/psi2023_pi_ecoconsumo'

app.config['SECRET_KEY'] = 'Jovial Bugle Storage'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(bp_usuario, url_prefix='/usuario')
app.register_blueprint(bp_doador, url_prefix='/doador')
app.register_blueprint(bp_empresa, url_prefix='/empresa')
app.register_blueprint(bp_administrador, url_prefix='/administrador')
app.register_blueprint(bp_vinculo, url_prefix='/vinculo')
app.register_blueprint(bp_entrega, url_prefix='/entrega')
app.register_blueprint(bp_premio, url_prefix='/premio')

db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)

# -------------------------- #


@app.route('/index')
@app.route('/home')
def index():
  return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.errorhandler(401)
def error(codigo):
  return redirect(url_for('usuario.logout'))

@app.route('/teste/<pag>')
def teste(pag):
    return render_template(f'{pag}.html')


## --- ##

@app.route('/')
@app.route('/zselecao')
def selecao():
  return render_template('zselecao.html')


@app.route('/zcadastro_consumidor')
def zcadastro_consumidor():
  return render_template('zcadastro-consumidor.html')

@app.route('/zcadastro_empresa')
def zcadastro_empresa():
  return render_template('zcadastro-empresa.html')


@app.route('/zlogin_consumidor')
def zlogin_consumidor():
  return render_template('zlogin-consumidor.html')

@app.route('/zlogin_empresa')
def zlogin_empresa():
  return render_template('zlogin-empresa.html')

@app.route('/zperfil_empresa')
def zperfil_empresa():
  return render_template('zperfil-empresa.html')




if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81, debug=True)
