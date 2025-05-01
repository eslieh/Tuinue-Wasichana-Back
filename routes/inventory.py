from flask import Blueprint, request, jsonify
from models import db, Inventory, Charity
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')


# GET: All inventory items for a specific charity
@inventory_bp.route('/charity/<int:charity_id>', methods=['GET'])
def get_inventory_for_charity(charity_id):
    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify({"error": "Charity not found."}), 404

    inventory_items = Inventory.query.filter_by(charity_id=charity_id).all()
    results = []
    for item in inventory_items:
        results.append({
            "id": item.id,
            "product": item.product,
            "quantity": item.product_quantity,
            "beneficiary": item.beneficiary_name,
            "date_added": item.created_at.strftime('%Y-%m-%d')
        })

    return jsonify(results), 200


# POST: Add a new inventory item
@inventory_bp.route('/', methods=['POST'])
def add_inventory():
    data = request.get_json()
    required_fields = ['charity_id', 'product', 'quantity', 'beneficiary']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields in request."}), 400

    charity = Charity.query.get(data['charity_id'])
    if not charity:
        return jsonify({"error": "Charity not found."}), 404

    new_item = Inventory(
        charity_id=charity.id,
        product=data['product'],
        product_quantity=data['quantity'],
        beneficiary_name=data['beneficiary']
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "message": "Inventory item added successfully.",
        "item": {
            "id": new_item.id,
            "product": new_item.product,
            "quantity": new_item.product_quantity,
            "beneficiary": new_item.beneficiary_name,
            "date_added": new_item.created_at.strftime('%Y-%m-%d')
        }
    }), 201
