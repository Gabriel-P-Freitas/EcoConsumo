from flask import Blueprint, request, jsonify, url_for
from utils.security import hash_password, check_password
from flask_jwt_extended import create_access_token
from utils.OAuth.google import google
from models.user import User, Doador, Empresa, Admin, db

bp = Blueprint('user', __name__)

@bp.route('/', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        users = User.query.all()

        data = [{
            'id': user.id,
            'user_type': user.user_type,
            'name': user.name,
            'email': user.email
        } for user in users]

        return jsonify({'data': data}), 200

    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        
        user_type = data.get('user_type').lower()
        hashed_password = hash_password(data.get('password'))

        if user_type == 'doador':
            user = Doador(
                name=data['name'],
                email=data['email'],
                password=hashed_password,
                birth_date=data.get('birth_date'),
                phone=data.get('phone')
            )
        elif user_type == 'empresa':
            user = Empresa(
                name=data['name'],
                email=data['email'],
                password=hashed_password,
                cnpj=data['cnpj'],
                phone=data.get('phone')
            )
        elif user_type == 'admin':
            user = Admin(
                name=data['name'],
                email=data['email'],
                password=hashed_password,
                access_level=data.get('access_level', 1)
            )
        else:
            return jsonify({'error': 'Invalid user type'}), 400

        db.session.add(user)
        db.session.commit()
        return jsonify({'message': f'{user_type} registered successfully'}), 201

@bp.route('/auth', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password(user.password, data['password']):
        return jsonify({'error': 'Incorret email or password.'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token}), 200
    

# @bp.route('/google/login')
# def google_login(): 
#     redirect_uri = url_for('user.google_authorize', _external=True)
#     return google.authorize_redirect(redirect_uri, prompt='select_account')

# @bp.route('/google/authorize')
# def google_authorize(): 
#     try:
#         token = google.authorize_access_token()   
#         user_info = google.get('userinfo').json() 
#         print(user_info)

#         doador = Doador.query.filter_by(email=user_info['email']).first()

#         if not doador:
#             doador = Doador(
#                 name=user_info['name'],
#                 email=user_info['email']
#             )
#             db.session.add(doador)
#             db.session.commit()

#         access_token = create_access_token(identity=doador.id)
#         return jsonify({'access_token': access_token}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
