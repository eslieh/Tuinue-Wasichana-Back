from flask import Blueprint, request, jsonify

donations_bp = Blueprint('donations', __name__)

donations = {}
donation_id_counter = 1

@donations_bp.route('/donations', methods=['POST'])
def create_donation():
    try:
        data = request.get_json()
        required_fields = ['donor_id', 'charity_id', 'amount']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        donation = Donations(**data)
        db.session.add(donation)
        db.session.commit()
        return jsonify(donation.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@donations_bp.route('/donations/<int:donation_id>', methods=['GET'])
def get_donation(donation_id):
    donation = Donations.query.get(donation_id)
    if not donation:
        return jsonify({'error': 'Donation not found'}), 404
    return jsonify(donation.to_dict())

@donations_bp.route('/donations', methods=['GET'])
def list_donations():
    donations = Donations.query.all()
    return jsonify([donation.to_dict() for donation in donations])

@donations_bp.route('/donations/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):
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
    try:
        donation = Donations.query.get(donation_id)
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        db.session.delete(donation)
        db.session.commit()
        return jsonify({'message': 'Donation deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
