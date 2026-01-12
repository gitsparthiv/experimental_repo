from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from app.extensions import db
from app.models import User
from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

# -----------------------
# Register
# -----------------------
@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    user = User(email=email)
    user.set_password(password)
    user.name = data.get('name', user.name)
    user.contact = data.get('contact', user.contact)

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered"}), 201


# -----------------------
# Login
# -----------------------
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


# -----------------------
# Profile
# -----------------------
@auth_bp.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(user.to_dict()), 200


@auth_bp.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json() or {}

    user.name = data.get('name', user.name)
    user.gender = data.get('gender', user.gender)
    user.contact = data.get('contact', user.contact)
    user.address = data.get('address', user.address)
    user.language = data.get('language', user.language)

    if 'age' in data:
        try:
            user.age = int(data['age']) if data['age'] else None
        except ValueError:
            return jsonify({"msg": "Invalid age"}), 400

    db.session.commit()
    return jsonify(user.to_dict()), 200


@auth_bp.route('/api/profile/health', methods=['PUT'])
@jwt_required()
def update_health():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json() or {}
    user.blood_group = data.get('blood_group', user.blood_group)
    user.blood_pressure = data.get('blood_pressure', user.blood_pressure)

    db.session.commit()
    return jsonify(user.to_dict()), 200


@auth_bp.route('/api/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json() or {}
    old = data.get('old_password')
    new = data.get('new_password')

    if not old or not new:
        return jsonify({"msg": "old_password and new_password required"}), 400

    if not user.check_password(old):
        return jsonify({"msg": "Old password incorrect"}), 401

    user.set_password(new)
    db.session.commit()
    return jsonify({"msg": "Password changed"}), 200