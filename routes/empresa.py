from flask import Blueprint, url_for, render_template, redirect, request, session
from api import api_request

bp = Blueprint('empresa', __name__)

@bp.route('/cadastro')
def cadastro():
    return render_template(f'empresa-cadastro.html')

@bp.route('/login')
def login():
    return render_template(f'empresa-login.html')

@bp.route('/perfil')
def perfil():
    token = session['token']
    data = api_request("GET", f"user/me", token)

    user_data = data.json().get('user_data')
    print(user_data)

    return render_template(f'empresa-perfil.html', user=user_data)