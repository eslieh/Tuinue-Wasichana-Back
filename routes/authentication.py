from flask import Blueprint, request, jsonify
from models import Admin, Donor, Charity, User, db
from utils import generate_verification_token, send_verification_email, redis_client


import json  # because we'll store dictionaries

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')  

    if not all([name, email, password, user_type]):
        return jsonify({"error": "Missing fields"}), 400

    token = generate_verification_token()

    pending_data = {
        "name": name,
        "password": password,
        "user_type": user_type,
        "token": token
    }

    # Store in Redis (key=email, value=json string)
    redis_client.setex(f"pending:{email}", 600, json.dumps(pending_data))  # expires after 10 minutes

    send_verification_email(email, token)

    return jsonify({"message": f"Verification token sent to {email}."}), 200

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')

    pending_data_raw = redis_client.get(f"pending:{email}")

    if not pending_data_raw:
        return jsonify({"error": "No pending registration for this email or token expired."}), 404

    pending_data = json.loads(pending_data_raw)

    if pending_data['token'] != token:
        return jsonify({"error": "Invalid token."}), 400

    # Token is correct, create the user
    name = pending_data['name']
    password = pending_data['password']
    user_type = pending_data['user_type']

    if user_type == 'admin':
        user = Admin(name=name, email=email)
    elif user_type == 'donor':
        user = Donor(name=name, email=email)
    elif user_type == 'charity':
        user = Charity(name=name, email=email)
    else:
        return jsonify({"error": "Invalid user type"}), 400

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # Clean up Redis
    redis_client.delete(f"pending:{email}")

    return jsonify({"message": "Account created successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Email and password are required."}), 400

    # Try to find the user (could be Admin, Donor, Charity)
    user = (
        Admin.query.filter_by(email=email).first() or
        Donor.query.filter_by(email=email).first() or
        Charity.query.filter_by(email=email).first()
    )

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    # (Optional) Here you would normally generate a session token or JWT
    return jsonify({
        "message": "Login successful!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "user_type": user.__class__.__name__.lower()
        }
    }), 200