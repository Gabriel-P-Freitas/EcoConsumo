from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.product import Product, db
from models.user import User


bp = Blueprint('product', __name__)

@bp.route('/', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in all_products])

@bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_product = Product(name=data['name'], price=data['price'], owner_id=user_id)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created"}), 201

@bp.route('/buy/<int:product_id>', methods=['POST'])
@jwt_required()
def buy_product(product_id):
    user_id = get_jwt_identity()
    product = Product.query.get_or_404(product_id)
    buyer = User.query.get(user_id)

    if buyer.balance < product.price:
        return jsonify({"error": "Insufficient balance"}), 400

    buyer.balance -= product.price
    db.session.commit()
    return jsonify({"message": "Product purchased successfully"}), 200
