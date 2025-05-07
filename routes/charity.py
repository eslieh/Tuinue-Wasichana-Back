from flask import Blueprint, request, jsonify
from models import Charity, Donation, Donor, User, db
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, get_jwt_identity

charity_bp = Blueprint('charity_bp', __name__, url_prefix='/charity')

@charity_bp.route('/', methods=['GET'])
def list_charities():
    charities = Charity.query.all()
    return jsonify([charity.to_dict() for charity in charities]), 200

@charity_bp.route('/<int:charity_id>', methods=['GET'])
def get_charity_details(charity_id):
    charity = Charity.query.options(
        joinedload(Charity.donations).joinedload(Donation.donor)
    ).filter_by(id=charity_id).first()

    if not charity:
        return jsonify({"error": "Charity not found"}), 404

    donations_data = []
    for donation in charity.donations:
        donor_name = "Anonymous" if donation.is_anonymous else donation.donor.name
        donations_data.append({
            "donor":        donor_name,
            "amount":       donation.amount,
            "is_recurring": donation.is_recurring,
            "status":       donation.status,
            "created_at":   donation.created_at.isoformat()
        })

    return jsonify({
        "id":                       charity.id,
        "user_name":               charity.name,
        "organisation_name":       charity.organisation_name,
        "organisation_description":charity.organisation_description,
        "goal":                    charity.goal,
        "logo_url":                charity.logo_url,
        "approved":                charity.approved,
        "donations":               donations_data
    }), 200

@charity_bp.route('/', methods=['POST'])
@jwt_required()
def create_or_update_charity_profile():
    identity = get_jwt_identity()
    user_id = identity.get('id')
    if not user_id:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    user = User.query.get(user_id)
    if not user or user.user_type != "charity":
        return jsonify({"error": "Only users with type 'charity' can create or update a charity profile."}), 403

    data = request.get_json() or {}

    # Try to fetch existing Charity row (profile)
    charity = Charity.query.get(user.id)
    if charity:
       # Otherwise, update existing (but blank) profile
        charity.organisation_name        = data.get('organisation_name', charity.organisation_name)
        charity.organisation_description = data.get('organisation_description', charity.organisation_description)
        charity.logo_url                 = data.get('logo_url', charity.logo_url)
        charity.goal                     = data.get('goal', charity.goal)
        db.session.commit()
        return jsonify(charity.to_dict()), 200

    # Create new Charity profile row linked to existing user
    new_charity = Charity(
        id=user.id,
        organisation_name=data.get("organisation_name"),
        organisation_description=data.get("organisation_description"),
        logo_url=data.get("logo_url"),
        goal=data.get("goal"),
        approved=False
    )
    db.session.add(new_charity)
    db.session.commit()

    return jsonify(new_charity.to_dict()), 201


@charity_bp.route('/<int:charity_id>', methods=['PUT'])
@jwt_required()
def update_charity(charity_id):
    identity = get_jwt_identity()
    user_id = identity.get('id')
    if not user_id:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    user = User.query.get(user_id)
    # Only the charity owner or an admin can update
    if not user or user.user_type != 'admin':
        return jsonify({"error": "Unauthorized to update charity."}), 403

    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify({"error": "Charity not found."}), 404

    # If charity user, ensure they own this profile
    if user.user_type == 'charity' and charity.id != user.id:
        return jsonify({"error": "You can only update your own charity profile."}), 403

    data = request.get_json() or {}
    # Update allowed fields
    charity.organisation_name = data.get('organisation_name', charity.organisation_name)
    charity.organisation_description = data.get('organisation_description', charity.organisation_description)
    charity.logo_url = data.get('logo_url', charity.logo_url)
    charity.goal = data.get('goal', charity.goal)
    charity.approved = data.get('approved', charity.approved)

    db.session.commit()

    return jsonify(charity.to_dict()), 200

@charity_bp.route('/<int:charity_id>', methods=['DELETE'])
@jwt_required()
def delete_charity(charity_id):
    identity = get_jwt_identity()
    user_id = identity.get('id')
    if not user_id:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    user = User.query.get(user_id)
    if not user or user.user_type not in ("charity", "admin"):
        return jsonify({"error": "Unauthorized to delete charity."}), 403

    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify({"error": "Charity not found."}), 404
    if user.user_type == 'charity' and charity.id != user.id:
        return jsonify({"error": "You can only delete your own charity profile."}), 403

    
    deleted = Charity.query.filter_by(id=charity_id).delete()
    db.session.commit()

    if deleted:
        return jsonify({"message": "Charity profile deleted successfully."}), 200
    else:
        return jsonify({"error": "Failed to delete charity profile."}), 500
