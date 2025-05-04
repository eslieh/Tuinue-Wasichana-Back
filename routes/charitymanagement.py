from flask import Blueprint, request, jsonify
from models import Charity, CharityApplication, User, db
from sqlalchemy.exc import SQLAlchemyError

charity_bp = Blueprint('charity_bp', __name__)

@charity_bp.route('/apply', methods=['POST'])
def apply_for_charity():
    data = request.get_json()
    try:
        
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            user_type="applicant"
        )
        new_user.set_password(data.get("password"))
        db.session.add(new_user)
        db.session.flush()

       
        new_application = CharityApplication(
            user_id=new_user.id,
            organisation_name=data.get("organisation_name"),
            organisation_description=data.get("organisation_description"),
            documents=data.get("documents"),  
            status="pending"
        )
        db.session.add(new_application)
        db.session.commit()
        
        return jsonify(new_application.to_dict()), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@charity_bp.route('/applications', methods=['GET'])
def get_applications():
    status = request.args.get('status', 'pending')
    applications = CharityApplication.query.filter_by(status=status).all()
    return jsonify([app.to_dict() for app in applications]), 200

@charity_bp.route('/applications/<int:app_id>', methods=['GET'])
def get_application(app_id):
    application = CharityApplication.query.get(app_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404
    return jsonify(application.to_dict()), 200

@charity_bp.route('/applications/<int:app_id>/approve', methods=['PATCH'])
def approve_application(app_id):
    try:
        application = CharityApplication.query.get(app_id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        
        user = User.query.get(application.user_id)
        user.user_type = "charity"

       
        new_charity = Charity(
            id=user.id,
            organisation_name=application.organisation_name,
            organisation_description=application.organisation_description,
            approved=True
        )
        db.session.add(new_charity)

        
        application.status = "approved"
        db.session.commit()

        return jsonify({
            "message": "Application approved and charity created",
            "charity": new_charity.to_dict()
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@charity_bp.route('/applications/<int:app_id>/reject', methods=['PATCH'])
def reject_application(app_id):
    application = CharityApplication.query.get(app_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404
    
    application.status = "rejected"
    db.session.commit()
    return jsonify({"message": "Application rejected"}), 200

@charity_bp.route('/applications/<int:app_id>', methods=['DELETE'])
def delete_application(app_id):
    application = CharityApplication.query.get(app_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404
    
    db.session.delete(application)
    db.session.commit()
    return jsonify({"message": "Application deleted"}), 200