from flask import Blueprint, request, jsonify
from models import db, Donation, Charity,Donor
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

donation_bp = Blueprint('donation', __name__)


@donation_bp.route('/test', methods=['GET'])
def get_test():
    return jsonify({"error":"error not here"}), 200


# GET: View all donations for a single charity
@donation_bp.route('/charity/<int:charity_id>', methods=['GET'])
def get_charity_donations(charity_id):
    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify({"error": "Charity not found."}), 404

    donations = Donation.query.filter_by(charity_id=charity_id).all()
    donation_list = []
    for donation in donations:
        donation_list.append({
            "id": donation.id,
            "donor_name": "Anonymous" if donation.is_anonymous else donation.donor.name,
            "amount": donation.amount,
            "frequency": donation.donor.donation_frequency,
            "date": donation.created_at.strftime('%Y-%m-%d')
        })

    return jsonify(donation_list), 200


@donation_bp.route('/donate', methods=['POST'])
@jwt_required()
def make_donation():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON data."}), 400

    required_fields = ['charity_id', 'amount', 'donation_frequency', 'is_anonymous']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 403

    # current = get_jwt_identity()
    donor_id = get_jwt_identity()
    if not donor_id:
        return jsonify({'error': 'You are not authenticated, please login'}), 401

    donor = Donor.query.get(donor_id)
    charity = Charity.query.get(data['charity_id'])

    if not donor:
        return jsonify({"error": "Donor not found."}), 404
    if not charity:
        return jsonify({"error": "Charity not found."}), 404

    donor.donation_frequency = data['donation_frequency']

    new_donation = Donation(
        amount=data['amount'],
        is_anonymous=data['is_anonymous'],
        is_recurring=(data['donation_frequency'].lower() != "one-time"),
        donor_id=donor_id,
        charity_id=charity.id,
        user_id=donor.id
    )

    db.session.add(new_donation)
    db.session.commit()

    return jsonify({
        "message": "Donation successful.",
        "donation": {
            "id": new_donation.id,
            "amount": new_donation.amount,
            "donor_name": "Anonymous" if new_donation.is_anonymous else donor.name,
            "frequency": donor.donation_frequency,
            "date": new_donation.created_at.strftime('%Y-%m-%d')
        }
    }), 201
