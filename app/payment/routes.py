from flask import Blueprint, request, jsonify
from app import db
from app.payment.models import Payment, Coupon
from datetime import datetime, timedelta, timezone

# before discount payment_bp

# payment_bp = Blueprint('payment', __name__)

# @payment_bp.route('/process', methods=['POST'])
# def process_payment():
#     data = request.get_json()
#     new_payment = Payment(
#         order_id=data['order_id'],
#         amount=data['amount'],
#         status='Completed' if data['success'] else 'Failed'
#     )
#     db.session.add(new_payment)
#     db.session.commit()
#     return jsonify({'message': 'Payment processed successfully' if data['success'] else 'Payment failed'}), 201

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/process', methods=['POST'])
def process_payment():
    data = request.get_json()
    order_id = data['order_id']
    amount = data['amount']
    success = data['success']

    # all elements are passed via class.
    new_payment = Payment(order_id=order_id, amount=amount, status='Completed' if success else 'Failed')
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment processed successfully' if success else 'Payment failed'}), 201

@payment_bp.route('/apply_coupon', methods=['POST'])
# def apply_coupon():
#     data = request.get_json()
#     code = data['code']
#     coupon = Coupon.query.filter_by(code=code).first()
#     if coupon and coupon.valid_until > db.func.current_timestamp():
#         return jsonify({'discount_percent': coupon.discount_percent}), 200
#     else:
#         return jsonify({'message': 'Invalid or expired coupon'}), 400
def apply_coupon():
    data = request.get_json()
    coupon_code = data.get('code') #       getting the code from the json response output.
    current_time = datetime.now(timezone.utc)

    # --------- unused, just for our reference -------------------------
    formatted_date_str = "%Y-%m-%d %H:%M:%S.%f"
    # valid_until_datetime = datetime.strptime(coupon.valid_until, formatted_date_str)
    if not coupon_code:
        return jsonify({'message': 'Coupon code is required'}), 400

    coupon = Coupon.query.filter_by(code=coupon_code).first()

    if not coupon:
        return jsonify({'message': 'Invalid coupon code'}), 404
    
    # to convert to string type formatted string.
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")

    # Check if the coupon is still valid
    #                                                                   to convert back the str to datetime.
    if coupon.valid_until and coupon.valid_until > datetime.strptime(current_time, formatted_date_str):
        # Apply coupon logic here
        return jsonify({'message': 'Coupon applied successfully'}), 200
    else:
        return jsonify({'message': 'Coupon has expired'}), 400


@payment_bp.route('/add_coupon', methods=['POST'])
def add_coupon():
    data = request.get_json()
    code = data['code']
    discount_percent = data['discount_percent']
    valid_until_str = data['valid_until']

    valid_until = datetime.fromisoformat(valid_until_str)
    new_coupon = Coupon(code=code, discount_percent=discount_percent, valid_until=valid_until)
    db.session.add(new_coupon)
    db.session.commit()
    return jsonify({'message': 'Coupon added successfully'}), 201

