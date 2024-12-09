from flask import Blueprint, request, jsonify, url_for
from utils.security import hash_password, check_password
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from utils.OAuth.google import google
from models.user import User, Doador, Empresa, Admin, db


bp = Blueprint('user', __name__)

@bp.route('/', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        users = User.query.all()

        data = []
        for user in users:
            user_variables = user.__dict__.copy()
            user_variables.pop('_sa_instance_state')
            user_variables.pop('password')
            
            data.append(user_variables)

        return jsonify({'users': data}), 200

    elif request.method == 'POST':
        data = request.get_json()
        
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
                name = data.get('name'),
                email = data.get('email'),
                password = hashed_password,
                cnpj = data.get('cnpj'),
                phone = data.get('phone'),

                address_cep = data.get('address_cep'),
                address_neighborhood = data.get('address_neighborhood'),
                address_street = data.get('address_street'),
                address_number = data.get('address_number')
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
    
@bp.route('/me', methods=['GET', 'POST'])
@jwt_required()
def me():
    if request.method == 'GET':
        user_id = get_jwt_identity()

        
        user = User.query.filter_by(id=user_id).first()
    
        if user.user_type == 'empresa':
            user = Empresa.query.filter_by(id=user_id).first()
        elif user.user_type == 'doador':
            user = Doador.query.filter_by(id=user_id).first()

        user_data = user.__dict__.copy()
        
        user_data.pop('_sa_instance_state')
        user_data.pop('password')

        return jsonify({'user_data': user_data}), 200

    elif request.method == 'POST':
        return "Não implementado"

@bp.route('/auth', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password(user.password, data['password']):
        return jsonify({'error': 'Incorret email or password.'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token}), 200
    
@bp.route('/oauth/google', methods=['GET', 'POST'])
def oauth_google(): 
    google_token = request.get_json()

    user_info = google.get('userinfo', token=google_token).json()
    print(user_info)
    email = user_info.get('email')
    name = f'{user_info.get("name")}'
    birth_date = user_info.get('birth_date')
    phone_number = user_info.get('phone_number')
    picture = user_info.get('picture')

    user = Doador.query.filter_by(email=email).first()
    if not user:
        user = Doador(
            name=name,
            email=email,
            password=None,
            birth_date=birth_date,
            phone=phone_number,
            picture=picture
        )

        db.session.add(user)
        db.session.commit()
    
    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token}), 200
