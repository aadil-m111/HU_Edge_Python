from flask import Blueprint, request, jsonify
from app import db
from app.cart.models import CartItem
from app.product.models import Product

cart_bp = Blueprint('cart', __name__)

# @cart_bp.route('/add', methods=['POST'])
# def add_to_cart():
#     data = request.get_json()
#     new_cart_item = CartItem(
#         user_id=data['user_id'],
#         product_id=data['product_id'],
#         quantity=data['quantity']
#     )
#     db.session.add(new_cart_item)
#     db.session.commit()
#     return jsonify({'message': 'Item added to cart'}), 201

# @cart_bp.route('/<int:user_id>', methods=['GET'])
# def get_cart(user_id):
#     cart_items = CartItem.query.filter_by(user_id=user_id).all()
#     return jsonify([{
#         'id': item.id,
#         'user_id': item.user_id,
#         'product_id': item.product_id,
#         'quantity': item.quantity
#     } for item in cart_items]), 200


# customisable cart:-

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data['user_id']
    product_id = data['product_id']
    quantity = data['quantity']

    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Check if the item is already in the cart
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        new_cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)

    db.session.commit()
    return jsonify({'message': 'Item added to cart successfully'}), 201

@cart_bp.route('/view/<int:user_id>', methods=['GET'])
def view_cart(user_id):
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    result = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        result.append({
            'product_id': item.product_id,
            'product_name': product.name,
            'quantity': item.quantity,
            'price': product.price
        })
    return jsonify(result), 200

@cart_bp.route('/update', methods=['PUT'])
def update_cart():
    data = request.get_json()
    user_id = data['user_id']
    product_id = data['product_id']
    quantity = data['quantity']

    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'message': 'Item not found in cart'}), 404

    cart_item.quantity = quantity
    db.session.commit()
    return jsonify({'message': 'Cart updated successfully'}), 200

@cart_bp.route('/remove', methods=['DELETE'])
def remove_from_cart():
    data = request.get_json()
    user_id = data['user_id']
    product_id = data['product_id']

    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'message': 'Item not found in cart'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart successfully'}), 200