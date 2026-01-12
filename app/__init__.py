# This file creates and configures the Flask app

import os
from datetime import timedelta
from dotenv import load_dotenv

from flask import Flask, jsonify, request
from flask_cors import CORS

from app.extensions import db, jwt
from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.symptom_routes import symptom_bp

def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # -----------------------
    # Configs
    # -----------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'change-this-secret-in-prod'
    app.config['JWT_SECRET_KEY'] = 'change-this-jwt-secret-in-prod'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

    # -----------------------
    # Init extensions
    # -----------------------
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()


    # -----------------------
    # JWT error handlers
    # -----------------------
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"msg": f"Invalid token: {error}"}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"msg": "Authorization token is missing"}), 401

    # -----------------------
    # Request logger
    # -----------------------
    @app.before_request
    def log_request_info():
        if request.path.startswith('/api/'):
            print(f"\n{'='*50}")
            print(f"📥 [FLASK] {request.method} {request.path}")
            if 'Authorization' in request.headers:
                auth_header = request.headers.get('Authorization')
                print(f"🔑 [FLASK] Auth header: {auth_header[:60]}...")
            print(f"{'='*50}\n")

    # -----------------------
    # Register blueprints (LAST)
    # -----------------------
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(symptom_bp)

    return app
