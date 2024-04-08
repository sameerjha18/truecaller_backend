from flask import Blueprint, request, jsonify, session
from api.models.model import User, db
from flask_bcrypt import check_password_hash
import re 


auth_bp = Blueprint('auth', __name__, url_prefix='/v1/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name').lower()
    email = data.get('email').lower()
    number = data.get('number')
    password = data.get('password').lower()

    rule = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email_validation = re.match(rule,email)
    if not email_validation:
        return jsonify({'error': 'Please, Insert valide email!!'}), 400
    
    pattern = re.compile(r'^\d{10}$')
    if not pattern.match(number):
        return jsonify({'error': 'Please, Insert valide Mobile number!!'}), 400


    if not name or not email or not number or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(mobile_number=number).first():
        return jsonify({'error': 'User already exists!'}), 409

    new_user = User(name=name, email=email, number=number, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    mobile = data.get('mobile')
    password = data.get('password').lower()

    if not mobile or not password:
        return jsonify({'error': 'Missing mobile number or password'}), 400

    user = User.query.filter_by(mobile_number=mobile).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid mobile number or password'}), 401
    
    session['user_id'] = user.id
    return jsonify({'message': 'Login successful'}), 200


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200
