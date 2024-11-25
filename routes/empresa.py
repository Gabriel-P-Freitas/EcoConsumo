from flask import Blueprint, url_for, render_template, redirect, request


bp = Blueprint('empresa', __name__)

@bp.route('/cadastro')
def cadastro():
    return render_template(f'empresa-cadastro.html')

@bp.route('/login')
def login():
    return render_template(f'empresa-login.html')

@bp.route('/perfil')
def perfil():
    return render_template(f'empresa-perfil.html')