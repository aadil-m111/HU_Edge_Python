from flask import Blueprint, request, jsonify
from app import db
from app.auth.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone, timedelta

# the below code is when we are moving forward for testing via data in memory:- 

# auth_bp = Blueprint('auth', __name__)

# users = {}

# @auth_bp.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()
#     username = data['username']
#     password = generate_password_hash(data['password'], method='pbkdf2:sha256')
#     email = data['email']

#     if username in users:
#         return jsonify({'message': 'User already exists'}), 400

#     users[username] = {'password': password, 'email': email}
#     return jsonify({'message': 'User created successfully'}), 201

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data['username']
#     password = data['password']

#     if username not in users or not check_password_hash(users[username]['password'], password):
#         return jsonify({'message': 'Invalid credentials'}), 401

#     token = jwt.encode({'username': username, 'exp': datetime.now(timezone.utc) + timedelta(hours=24)}, 'your_secret_key', algorithm='HS256')
#     return jsonify({'token': token}), 200


# =================================================================================

# data in database saving:-

auth_bp = Blueprint('auth', __name__)

# to create a new user in the database
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# authenticates the user from the database itself and generates a jwt token if the credentials are correct.
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({'username': username, 'exp': datetime.now(timezone.utc) + timedelta(hours=24)}, 'your_secret_key', algorithm='HS256')
    return jsonify({'token': token}), 200

