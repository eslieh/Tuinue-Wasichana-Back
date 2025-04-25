from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models.inventory import Inventory
from ..models.charity import Charity
from .. import db

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/inventory', methods=['POST'])
def create_delivery():
    try:
        data = request.get_json()
        new_delivery = Inventory(
            charity_id=data['charity_id'],
            product=data['product'],
            product_quantity=data['product_quantity'],
            beneficiary_name=data['beneficiary_name']
        )
        db.session.add(new_delivery)
        db.session.commit()
        return jsonify(new_delivery.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@inventory_bp.route('/inventory', methods=['GET'])
def get_all_deliveries():
    try:
        deliveries = Inventory.query.all()
        return jsonify([delivery.to_dict() for delivery in deliveries]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@inventory_bp.route('/charities/<int:charity_id>/inventory', methods=['GET'])
def get_charity_inventory(charity_id):
    try:
        charity = Charity.query.get(charity_id)
        if not charity:
            return jsonify({'error': 'Charity not found'}), 404
        deliveries = Inventory.query.filter_by(charity_id=charity_id).all()
        return jsonify([delivery.to_dict() for delivery in deliveries]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400