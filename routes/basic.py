from flask import Blueprint, url_for, render_template, redirect, request


bp = Blueprint('basic', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for('basic.selecao'))

@bp.route('/teste/<arq>')
def test(arq):
    return render_template(f'{arq}.html')


@bp.route('/selecao')
def selecao():
    return render_template(f'selecao.html')


