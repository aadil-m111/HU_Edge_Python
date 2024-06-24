from flask import Blueprint, request, jsonify
from app import db
from app.product.models import Product

product_bp = Blueprint('product', __name__)

@product_bp.route('/all', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity
    } for product in products]), 200

@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'}), 201