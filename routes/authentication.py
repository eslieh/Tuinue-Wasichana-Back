import json
import redis
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from models import Admin, Donor, Charity, db
from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from models import Admin, Donor, Charity, User, db
from utils import generate_verification_token, send_verification_email, redis_client
from datetime import timedelta
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    if not all([name, email, password, user_type]):
        return jsonify({"error": "Missing fields"}), 400

    token = generate_verification_token()
    pending = {"name": name, "password": password, "user_type": user_type, "token": token}
    try:
        redis_client.setex(f"pending:{email}", 600, json.dumps(pending))
    except Exception:
        return jsonify({"error": "Verification service unavailable."}), 503

    send_verification_email(email, token)
    return jsonify({"message": f"Verification token sent to {email}."}), 200

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.get_json() or {}
    email = data.get('email')
    token = data.get('token')
    if not all([email, token]):
        return jsonify({"error": "Email and token required."}), 400
    try:
        raw = redis_client.get(f"pending:{email}")
    except Exception:
        return jsonify({"error": "Verification service unavailable."}), 503

    if not raw:
        return jsonify({"error": "No pending registration or token expired."}), 404

    try:
        raw = redis_client.get(f"pending:{email}")
    except Exception:
        return jsonify({"error": "Verification service unavailable."}), 503

    if not raw:
        return jsonify({"error": "No pending registration or token expired."}), 404

    pending = json.loads(raw)
    if pending.get('token') != token:
        return jsonify({"error": "Invalid token."}), 400

    name, pwd, utype = pending["name"], pending["password"], pending["user_type"]
    # Token is correct, create the user
    name, pwd, utype = pending["name"], pending["password"], pending["user_type"]

    if utype == 'admin':
        user = Admin(name=name, email=email)
    elif utype == 'donor':
        user = Donor(name=name, email=email)
    elif utype == 'charity':
        user = Charity(name=name, email=email)
    else:
        return jsonify({"error": "Invalid user type"}), 400

    user.set_password(pwd)
    db.session.add(user)
    db.session.commit()
    try:
        redis_client.delete(f"pending:{email}")
    except Exception:
        pass

    raw_token = create_access_token(
        identity={
            'id': user.id,
            'email': user.email,
            'user_type': user.__class__.__name__.lower()
        },
        expires_delta=timedelta(days=1)
    )
    # Ensure token is a str for JSON serialization
    if isinstance(raw_token, (bytes, bytearray, memoryview)):
        access_token = raw_token.decode('utf-8')
    else:
        access_token = str(raw_token)
        
    return jsonify({
        "message": "Account created successfully!",
        "access_token": access_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
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

    raw_token = create_access_token(
        identity={
            'id': user.id,
            'email': user.email,
            'user_type': user.__class__.__name__.lower()
        },
        expires_delta=timedelta(days=1)
    )
    if isinstance(raw_token, (bytes, bytearray, memoryview)):
        access_token = raw_token.decode('utf-8')
    else:
        access_token = str(raw_token)    
    
    session['user_id'] = user.id
    session['user_type'] = user.__class__.__name__.lower()

    return jsonify({
        "message": "Login successful!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "user_type": user.__class__.__name__.lower()
        },
        "access_token" : access_token
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current = get_jwt_identity()
    if not current:
        return jsonify({
            "error":"user not authenticate"
        }), 403
    
    return jsonify({
        "id": current.get('id'),
        "email": current.get('email'),
        "user_type": current.get('user_type')
    }), 200
