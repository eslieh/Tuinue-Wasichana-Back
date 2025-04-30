from flask import Blueprint, request, jsonify,session
from models import Charity, Donation, Donor, User, db
from sqlalchemy.orm import joinedload

charity_bp = Blueprint('charities', __name__)

@charity_bp.route('/', methods=['GET'])
def list_charities():
    charities = Charity.query.all()
    return jsonify([charity.to_dict() for charity in charities]), 200

@charity_bp.route('/<int:charity_id>', methods=['GET'])
def get_charity_details(charity_id):
    charity = Charity.query.options(joinedload(Charity.donations).joinedload(Donation.donor)).filter_by(id=charity_id).first()

    if not charity:
        return jsonify({"error": "Charity not found"}), 404

    donations_data = []
    for donation in charity.donations:
        donor_name = "Anonymous" if donation.is_anonymous else donation.donor.name
        donations_data.append({
            "donor": donor_name,
            "amount": donation.amount,
            "is_recurring": donation.is_recurring,
            "status": donation.status,
            "created_at": donation.created_at.isoformat()
        })

    return jsonify({
        "id": charity.id,
        "name": charity.name,
        "description": charity.organisation_description,
        "donations": donations_data
    }), 200

@charity_bp.route('/', methods=['POST'])
def create_charity_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    user = User.query.get(user_id)

    if not user or user.user_type != "charity":
        return jsonify({"error": "Only users with type 'charity' can create a charity profile."}), 403

    data = request.get_json()

    # Check if charity profile already exists
    if user.charity_profile:
        charity = user.charity_profile

        # Ensure charity profile is not fully created already
        if charity.organisation_name or charity.organisation_description or charity.logo_url:
            return jsonify({"error": "Charity profile already exists for this user."}), 400

        # Update the existing charity profile
        charity.organisation_name = data.get("organisation_name")
        charity.organisation_description = data.get("organisation_description")
        charity.logo_url = data.get("logo_url")

        db.session.commit()  # Commit only charity changes
        return jsonify(charity.to_dict()), 200

    # Create a new charity profile if none exists
    charity = Charity(
        id=user.id,
        organisation_name=data.get("organisation_name"),
        organisation_description=data.get("organisation_description"),
        logo_url=data.get("logo_url")
    )
    charity.user = user

    db.session.add(charity)  # Add charity only, don't modify the user here
    db.session.commit()  # Commit only charity changes

    return jsonify(charity.to_dict()), 201
