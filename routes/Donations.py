from flask import Blueprint, request, jsonify
from models import db, Donation, Charity, Donor
from datetime import datetime

donation_bp = Blueprint('donation', __name__, url_prefix='/donations')


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


# POST: Donor makes a donation to a charity
@donation_bp.route('/', methods=['POST'])
def make_donation():
    data = request.get_json()

    required_fields = ['donor_id', 'charity_id', 'amount', 'donation_frequency', 'is_anonymous']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 400

    donor = Donor.query.get(data['donor_id'])
    charity = Charity.query.get(data['charity_id'])

    if not donor:
        return jsonify({"error": "Donor not found."}), 404
    if not charity:
        return jsonify({"error": "Charity not found."}), 404

    # Update donation frequency on donor profile
    donor.donation_frequency = data['donation_frequency']

    new_donation = Donation(
        amount=data['amount'],
        is_anonymous=data['is_anonymous'],
        is_recurring=(data['donation_frequency'].lower() != "one-time"),
        donor=donor,
        charity=charity,
        user=donor  # link to user as well
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
