from flask import Blueprint, request, jsonify, session
from API.models.model import User, db
from flask_bcrypt import check_password_hash


auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name').lower()
    email = data.get('email').lower()
    number = data.get('number').lower()
    password = data.get('password').lower()

    if not name or not email or not number or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists!'}), 409

    new_user = User(name=name, email=email, number=number, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email').lower()
    password = data.get('password').lower()

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    session['user_id'] = user.id
    return jsonify({'message': 'Login successful'}), 200


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200