from flask import Blueprint, request, jsonify, session
from api.models.model import User
import re
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/v1/api')

bcrypt = Bcrypt()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    mobile = data.get('number')
    password = data.get('password')

    if not name or not email or not mobile or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    rule = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email_validation = re.match(rule, email)
    if not email_validation:
        return jsonify({'error': 'Please, Insert valid email!!'}), 400

    pattern = re.compile(r'^\d{10}$')
    if not pattern.match(mobile):
        return jsonify({'error': 'Please, Insert valid Mobile number!!'}), 400

    existing_user = User.objects(mobile_number=mobile).first()
    if existing_user:
        return jsonify({'error': 'User already exists!'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        new_user = User(full_name=name.lower(), email=email.lower(), mobile_number=mobile, password=hashed_password)
        new_user.save()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    mobile = data.get('mobile')
    password = data.get('password').lower()

    if not mobile or not password:
        return jsonify({'error': 'Missing mobile number or password'}), 400

    user = User.objects(mobile_number=mobile).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid mobile number or password'}), 401

    session['user_id'] = str(user.id)
    return jsonify({'message': 'Login successful'}), 200


#
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

