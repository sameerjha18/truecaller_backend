from flask import Blueprint, request, jsonify,session,abort,current_app
from API.models.model  import User, db


user_bp = Blueprint('user', __name__, url_prefix='/api/user')
#List down Users
@user_bp.route('/users', methods=['GET'])
def user_list():
    users = User.query.all()
    users_list = [{'id':user.id, 'name': user.full_name, 'email': user.email, 'Mobile': user.mobile_number} for user in users]
    return jsonify(users_list), 200

#Single Profile
@user_bp.route('/profile', methods=['GET'])
def profile():
    if 'user_id' in session:
        name = request.args.get('name')
        if not name:
            return jsonify({'error': 'Profile name parameter is missing'}), 400
        
        user = User.query.filter_by(full_name=name).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'id': user.id, 'name': user.full_name, 'mobile': user.mobile_number, 'email': user.email}), 200
    else:
        return jsonify({'error': 'You are not logged in'}), 401

@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    user_id = request.args.get('user_id')
    if 'user_id' not in session:
        current_app.logger.debug("User ID not found in session.")
        abort(401)  # Unauthorized
    
    if int(user_id) != session['user_id']:
        current_app.logger.debug(f"user_id: {user_id}, session['user_id']: {session['user_id']}")
        abort(403)  # Forbidden, user can only update their own profile

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    name = data.get('name', user.full_name)
    email = data.get('email', user.email)
    mobile = data.get('number', user.mobile_number)

    user.full_name = name
    user.email = email
    user.mobile_number = mobile

    db.session.commit()

    return jsonify({'message': 'User details updated successfully'}), 200