from flask import Blueprint, jsonify
from models.charity import Charity, CharityApplication
from models.user import User
from models.story import Story
from config import db
from sqlalchemy.exc import SQLAlchemyError
from auth import admin_required

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/charities/<int:charity_id>', methods=['DELETE'])
@admin_required
def delete_charity(charity_id):
    try:
        charity = Charity.query.get(charity_id)
        if not charity:
            return jsonify({"error": "Charity not found"}), 404

        
        Story.query.filter_by(charity_id=charity_id).delete()

        
        db.session.delete(charity)

        
        user = User.query.get(charity_id)
        if user:
            user.user_type = "user"
            db.session.add(user)

        db.session.commit()
        return jsonify({"message": "Charity and all associated data deleted"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500