from flask import Blueprint, request, jsonify, session, abort
from api.models.model import BlockedNumber
import re

call_bp = Blueprint('call', __name__, url_prefix='/v1/api/calls')


@call_bp.route('/block', methods=['POST'])
def block():
    if 'user_id' in session:
        data = request.get_json()
        user_id = session['user_id']
        mobile = data.get('number')

        if not mobile or not user_id:
            return jsonify({'error': 'Missing required fields'}), 400

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(mobile):
            return jsonify({'error': 'Please, Insert valid Mobile number!!'}), 400

        if BlockedNumber.objects(user_id=user_id, reported_number=mobile).first():
            return jsonify({'error': 'Number already Blocked!'}), 409

        block_number = BlockedNumber(user_id=user_id, reported_number=mobile)
        block_number.save()
        return jsonify({'message': 'Number Blocked successfully'}), 201
    else:
        return jsonify({'error': 'You are not logged in'}), 401


@call_bp.route('/unblock', methods=['POST'])
def unblock():
    user_id = request.args.get('user_id')
    if 'user_id' not in session or str(user_id) != session['user_id']:
        abort(401)  # Unauthorized

    data = request.get_json()
    mobile_number = data.get('number')

    if not mobile_number:
        return jsonify({'error': 'Mobile number is required'}), 400

    pattern = re.compile(r'^\d{10}$')
    if not pattern.match(mobile_number):
        return jsonify({'error': 'Please, Insert valid Mobile number!!'}), 400

    # Check if the mobile number is reported by the user
    blocked = BlockedNumber.objects(user_id=str(user_id), reported_number=mobile_number).first()
    if not blocked:
        return jsonify({'error': 'Mobile number is not Blocked'}), 400

    # Unblock the mobile number by deleting the documents
    blocked.delete()

    return jsonify({'message': 'Mobile number unblocked successfully'}), 200
