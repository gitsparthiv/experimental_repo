import os
from datetime import timedelta
from dotenv import load_dotenv

from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai

from app.extensions import db, jwt
from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.symptom_routes import symptom_bp
from app.routes.emergency_chat_routes import emergency_chat_bp


def create_app():
    # -----------------------
    # Load environment
    # -----------------------
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # -----------------------
    # Config
    # -----------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(BASE_DIR, "app.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "dev-jwt-secret"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
    )

    # -----------------------
    # Init extensions
    # -----------------------
    db.init_app(app)
    jwt.init_app(app)

    # -----------------------
    # Gemini (ONE place)
    # -----------------------
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        genai.configure(api_key=gemini_key)
        app.gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")
    else:
        app.gemini_model = None
        print("⚠️ GEMINI_API_KEY not set")

    # -----------------------
    # Create tables (dev only)
    # -----------------------
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
    # Request logger (optional)
    # -----------------------
    @app.before_request
    def log_request_info():
        if request.path.startswith("/api/"):
            print(f"\n{'='*50}")
            print(f"📥 {request.method} {request.path}")
            if "Authorization" in request.headers:
                print("🔑 Auth header present")
            print(f"{'='*50}\n")

    # -----------------------
    # Register blueprints
    # -----------------------
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(symptom_bp)
    app.register_blueprint(emergency_chat_bp)

    # -----------------------
    # Health check
    # -----------------------
    @app.route("/health")
    def health():
        return {
            "db": "ok",
            "gemini": bool(app.gemini_model)
        }, 200

    return app
