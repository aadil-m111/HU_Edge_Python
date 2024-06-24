from flask import Blueprint, request, jsonify
from app import db
from app.order.models import Order

# before discount:- 

# order_bp = Blueprint('order', __name__)

# @order_bp.route('/create', methods=['POST'])
# def create_order():
#     data = request.get_json()
#     new_order = Order(
#         user_id=data['user_id'],
#         total_price=data['total_price'],
#         status='Pending'
#     )
#     db.session.add(new_order)
#     db.session.commit()
#     return jsonify({'message': 'Order created successfully'}), 201

# @order_bp.route('/<int:user_id>', methods=['GET'])
# def get_orders(user_id):
#     orders = Order.query.filter_by(user_id=user_id).all()
#     return jsonify([{
#         'id': order.id,
#         'user_id': order.user_id,
#         'total_price': order.total_price,
#         'status': order.status,
#         'created_at': order.created_at
#     } for order in orders]), 200


order_bp = Blueprint('order', __name__)

@order_bp.route('/create', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data['user_id']
    total_price = data['total_price']
    discount = data.get('discount', 0.0)
    status = 'Pending'

    new_order = Order(user_id=user_id, total_price=total_price, discount=discount, status=status)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@order_bp.route('/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': order.id,
        'user_id': order.user_id,
        'total_price': order.total_price,
        'discount': order.discount,
        'status': order.status,
        'created_at': order.created_at
    } for order in orders]), 200