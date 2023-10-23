from flask import Flask, render_template, request, redirect

app = Flask(__name__)

usuarios = []
usuarios_conectados = []
usuario_atual = [None]

@app.route('/') 
def home():
  return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  mensagens = []
  
  if request.method == 'POST':
    email = request.form.get('email')
    senha = request.form.get('senha')

    for usuario in usuarios:
      if usuario['email'] == email and usuario['senha'] == senha:
        if usuario not in usuarios_conectados:
          usuarios_conectados.append(usuario)
          usuario_atual.clear()
          usuario_atual.append(usuario)
          return redirect('/perfil')
        elif usuario_atual[0] != usuario:
          usuario_atual.clear()
          usuario_atual.append(usuario)
          return redirect('/perfil')
        else:
          mensagens.append('Usuario já está conectado')
        break
    else:
      mensagens.append('Email ou Senha incorretos.')

  return render_template('login.html', mensagens=mensagens)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

  mensagens = []
  
  if request.method == 'POST':
    tipo = request.form.get('tipo')
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    for usuario in usuarios:
      if usuario['nome'] == nome or usuario['email'] == email:
        mensagens.append('Já existe um usuario com o Nome ou Email informado')
        break
    else:
      usuario = {'nome': nome, 'email': email, 'senha': senha, 'tipo': tipo}
      usuarios.append(usuario)
      mensagens.append('Usuario cadastrado com sucesso!')
  
  return render_template('cadastro.html', mensagens=mensagens)


@app.route('/buscar')
def buscar():
  users = []

  if usuario_atual[0]:
    if usuario_atual[0]['tipo'] == 'instituicao':
      busca = 'doador'
    else:
      busca = 'instituicao'

    for usuario in usuarios:
        if usuario['tipo'] == busca:
          users.append(usuario)
  else:
    users = usuarios

  print(users)  
  return render_template('buscar.html', users=users)


@app.route('/perfil')
def perfil():
  return render_template('perfil.html', user=usuario_atual[0])


app.run(host='0.0.0.0', port=81, debug=True)

