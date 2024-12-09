from flask import Blueprint, url_for, render_template, redirect, request, session
from api import api_request
from utils.oauth.google import google, oauth
import requests


bp = Blueprint('usuario', __name__)

@bp.route('/autenticar', methods=['GET', 'POST'])
def autenticar():
    print('AUTENTICAR')
    if request.method == 'GET':
        try: 
            token = google.authorize_access_token()
            response = api_request('POST', 'user/oauth/google', data=token)
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                session['token'] = access_token
                return redirect(url_for('doador.perfil'))
        except KeyError as e:
            print(e)
        
        return redirect(url_for('basic.selecao'))
    
    elif request.method == 'POST':
        # Obter dados
        user_type = request.args.get('user_type')

        email = request.form.get('email')
        password = request.form.get('senha')

        data = {
            "email": email,
            "password": password,
        }

        # Enviar para API
        response = api_request('POST', 'user/auth', data=data)
        if response.status_code == 200:
            token = response.json().get('access_token')
            session['token'] = token

            if user_type == 'empresa':
                return redirect(url_for('empresa.perfil'))
            if user_type == 'doador':
                return redirect(url_for('doador.perfil'))
            
            return redirect(url_for('basic.index'))
        
        print(f'ERRO {response.status_code} {response.text}')
        return redirect(request.referrer)

@bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    print('CADASTRAR')
    if request.method == 'GET':
        return redirect(url_for('basic.selecao'))
    
    elif request.method == 'POST':
        # Obter dados
        user_type = request.args.get('user_type')

        name = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('senha')
        phone = request.form.get('telefone', '')

        birth_date = request.form.get('nascimento', '')
        cnpj = request.form.get('cnpj', '')

        cep = request.form.get('cep', '')
        bairro = request.form.get('bairro', '')
        rua = request.form.get('rua', '')
        numero = request.form.get('numero', '')
        
        data = {
            "user_type": user_type,
            "name": name,
            "email": email,
            "password": password,

            "birth_date": birth_date,
            "phone": phone,
            "cnpj": cnpj,

            "address_cep": cep,
            "address_neighborhood": bairro,
            "address_street": rua,
            "address_number": numero
        }

        # Enviar para API
        response = api_request('POST', 'user', data=data)
        if response.status_code == 201:
            return redirect(url_for('basic.selecao'))
        
        #print(f'ERRO {response.status_code} {response.text}')
        return redirect(request.referrer)
    
@bp.route('/oauth/google', methods=['GET', 'POST'])
def oauth_google():
    print('OAuth Google')

    redirect_uri = url_for('usuario.autenticar', _external=True)
    return google.authorize_redirect(redirect_uri, prompt='select_account')
