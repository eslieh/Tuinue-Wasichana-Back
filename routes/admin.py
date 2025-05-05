from flask import Blueprint, jsonify, request, abort
from models import db, User, Donor, Charity, Donation
from sqlalchemy.orm import joinedload

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# Get all users with details
@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = []

    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "user_type": user.user_type,
            "created_at": user.created_at,
        }

        if isinstance(user, Charity):
            user_data.update({
                "organisation_name": user.organisation_name,
                "organisation_description": user.organisation_description,
                "logo_url": user.logo_url,
            })

        elif isinstance(user, Donor):
            user_data.update({
                "donation_frequency": user.donation_frequency,
                "reminder_enabled": user.reminder_enabled,
                "donations": [
                    {
                        "amount": d.amount,
                        "charity": d.charity.organisation_name if d.charity else "Unknown",
                        "is_recurring": d.is_recurring,
                        "is_anonymous": d.is_anonymous,
                        "status": d.status,
                        "date": d.created_at.strftime('%Y-%m-%d')
                    } for d in user.donations
                ]
            })

        result.append(user_data)

    return jsonify(result), 200


# Delete user by ID (admin-only)
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user.name} deleted successfully."}), 200
