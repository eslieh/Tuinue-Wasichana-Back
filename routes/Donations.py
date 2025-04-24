from flask import Blueprint, request, jsonify

donations_bp = Blueprint('donations', __name__)

donations = {}
donation_id_counter = 1

@donations_bp.route('/donations', methods=['POST'])
def create_donation():
    global donation_id_counter
    data = request.get_json()
    required_fields = ['donor_id', 'charity_id', 'amount', 'donation_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    donation = {
        'id': donation_id_counter,
        'donor_id': data['donor_id'],
        'charity_id': data['charity_id'],
        'amount': data['amount'],
        'donation_type': data['donation_type'],  # e.g, one-time or monthly
        'timestamp': data.get('timestamp')
    }
    donations[donation_id_counter] = donation
    donation_id_counter += 1
    return jsonify(donation), 201 #success status code

@donations_bp.route('/donations/<int:donation_id>', methods=['GET'])
def get_donation(donation_id):
    donation = donations.get(donation_id)
    if not donation:
        return jsonify({'error': 'Donation not found'}), 404 # client‑error status code
    return jsonify(donation)

@donations_bp.route('/donations', methods=['GET'])
def list_donations():
    return jsonify(list(donations.values()))

@donations_bp.route('/donations/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):client‑error status code
    donation = donations.get(donation_id)
    if not donation:
        return jsonify({'error': 'Donation not found'}), 404
    data = request.get_json()
    # This Allows updating amount and donation_type only for simplicity
    if 'amount' in data:
        donation['amount'] = data['amount']
    if 'donation_type' in data:
        donation['donation_type'] = data['donation_type']
    return jsonify(donation)

@donations_bp.route('/donations/<int:donation_id>', methods=['DELETE'])
def delete_donation(donation_id):
    if donation_id in donations:
        del donations[donation_id]
        return jsonify({'message': 'Donation deleted'})
    else:
        return jsonify({'error': 'Donation not found'}), 404
