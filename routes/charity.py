from flask import Blueprint, request, jsonify
from models.charity import Charity
from models.user import User
from config import db  
from sqlalchemy.exc import SQLAlchemyError

charity_bp = Blueprint('charity_bp', __name__, url_prefix='/charities')


@charity_bp.route('', methods=['POST'])
def create_charity():
    data = request.get_json()
    try:
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            user_type="charity"
        )
        new_user.set_password(data.get("password"))
        db.session.add(new_user)
        db.session.flush()  

        charity = Charity(
            id=new_user.id, 
            organisation_name=data.get("organisation_name"),
            organisation_description=data.get("organisation_description"),
            logo=data.get("logo"),
            approved=False
        )
        db.session.add(charity)
        db.session.commit()
        return jsonify(charity.to_dict()), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@charity_bp.route('/<int:id>', methods=['GET'])
def get_charity(id):
    charity = Charity.query.get(id)
    if not charity:
        return jsonify({"error": "Charity not found"}), 404
    return jsonify(charity.to_dict()), 200


@charity_bp.route('/<int:id>', methods=['PUT'])
def update_charity(id):
    data = request.get_json()
    charity = Charity.query.get(id)
    if not charity:
        return jsonify({"error": "Charity not found"}), 404

    charity.organisation_name = data.get("organisation_name", charity.organisation_name)
    charity.organisation_description = data.get("organisation_description", charity.organisation_description)
    charity.logo = data.get("logo", charity.logo)

    db.session.commit()
    return jsonify(charity.to_dict()), 200


@charity_bp.route('', methods=['GET'])
def list_charities():
    charities = Charity.query.filter_by(approved=True).all()
    return jsonify([charity.to_dict() for charity in charities]), 200


@charity_bp.route('/<int:id>/approve', methods=['PATCH'])
def approve_charity(id):
    charity = Charity.query.get(id)
    if not charity:
        return jsonify({"error": "Charity not found"}), 404

    charity.approved = True
    db.session.commit()
    return jsonify({"message": "Charity approved", "charity": charity.to_dict()}), 200
