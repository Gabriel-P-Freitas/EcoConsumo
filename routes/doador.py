from flask import Blueprint, url_for, render_template, redirect, request


bp = Blueprint('doador', __name__)

@bp.route('/cadastro')
def cadastro():
    return render_template(f'doador-cadastro.html')

@bp.route('/login')
def login():
    return render_template(f'doador-login.html')