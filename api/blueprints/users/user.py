from flask import Blueprint, request, jsonify, session, abort, current_app
from api.models.model import User
import re

user_bp = Blueprint('user', __name__, url_prefix='/v1/api/user')


# List down Users
@user_bp.route('/users', methods=['GET'])
def user_list():
    users_list = [{'id': str(user.id), 'name': user.full_name, 'email': user.email, 'mobile': user.mobile_number} for
                  user in User.objects()]
    return jsonify(users_list), 200


# #Single Profile
@user_bp.route('/profile', methods=['GET'])
def profile():
    if 'user_id' in session:
        name = request.args.get('name')
        if not name:
            return jsonify({'error': 'Profile name parameter is missing'}), 400

        user = User.objects(full_name=name.lower()).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'id': str(user.id), 'name': user.full_name, 'mobile': user.mobile_number, 'email': user.email}), 200
    else:
        return jsonify({'error': 'You are not logged in'}), 401


@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    user_id = request.args.get('user_id')
    if 'user_id' not in session:
        current_app.logger.debug("User ID not found in session.")
        abort(401)  # Unauthorized

    if str(user_id) != str(session['user_id']):
        current_app.logger.debug(f"user_id: {user_id}, session['user_id']: {session['user_id']}")
        abort(403)  # Forbidden, user can only update their own profile

    user = User.objects(id=user_id).first()
    if not user:
        abort(404)
    data = request.get_json()
    name = data.get('name', user.full_name)
    email = data.get('email', user.email)
    mobile = data.get('number', user.mobile_number)

    pattern = re.compile(r'^\d{10}$')
    if not pattern.match(mobile):
        return jsonify({'error': 'Please, Insert valid Mobile number!!'}), 400

    user.full_name = name.lower()
    user.email = email.lower()
    user.mobile_number = mobile

    user.save()

    return jsonify({'message': 'User details updated successfully'}), 200
