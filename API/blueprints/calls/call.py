from flask import Blueprint, request, jsonify,session,abort
from API.models.model  import Blocked_number, db

call_bp = Blueprint('call', __name__, url_prefix='/api/calls')

@call_bp.route('/block', methods=['POST'])
def block():
    if 'user_id' in session:
        data = request.get_json()
        user_id = session['user_id']
        number = data.get('number')

        if not number or not user_id:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if Blocked_number.query.filter_by(reported_number=number).first():
            return jsonify({'error': 'Number already Bloacked!'}), 409
        
        block_number = Blocked_number(user_id=user_id, reported_number=number)
        db.session.add(block_number)
        db.session.commit()
        return jsonify({'message': 'Number Blocked successfully'}), 201
    else:
        return jsonify({'error': 'You are not logged in'}), 401
    

@call_bp.route('/unblock', methods=['POST'])
def unblock():
    user_id = request.args.get('user_id')
    if 'user_id' not in session or int(user_id) != session['user_id']:
        abort(401)  # Unauthorized
    
    data = request.get_json()
    mobile_number = data.get('number')

    if not mobile_number:
        return jsonify({'error': 'Mobile number is required'}), 400

    # Check if the mobile number is reported by the user
    blocked = Blocked_number.query.filter_by(user_id=int(user_id), reported_number=mobile_number).first()
    if not blocked:
        return jsonify({'error': 'Mobile number is not Blocked'}), 400

    # Unblock the mobile number by deleting the report
    db.session.delete(blocked)
    db.session.commit()

    return jsonify({'message': 'Mobile number unblocked successfully'}), 200