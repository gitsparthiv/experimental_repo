import os     #Gives access to OS-level features for reading environment variables and building file paths safely
from datetime import timedelta   #Used to define time durations, here JWT token expiry (30 days)
from dotenv import load_dotenv   #Loads environment variables from a .env file into memory

from flask import Flask, jsonify, request     #Flask → creates the app, jsonify → returns JSON responses, request → access incoming HTTP request data
from flask_cors import CORS     #Required when frontend & backend are on different origins
import google.generativeai as genai    #Google Gemini AI SDK, Used later to configure and create the AI model

from app.extensions import db, jwt     #import shared extensions: db → SQLAlchemy database instance, jwt → Flask-JWT-Extended instance
from app.routes.main_routes import main_bp      #Imports Blueprints where each blueprint contains related routes and they will be registered later
from  app.routes.auth_routes import auth_bp
from app.routes.symptom_routes import symptom_bp
from app.routes.emergency_chat_routes import emergency_chat_bp

def create_app():
    # -----------------------
    # Load environment
    # -----------------------
    load_dotenv()        #Reads .env, Makes values available via os.getenv()

    app = Flask(__name__)      #Creates the Flask application instance, __name__ helps Flask locate files/resources
    CORS(app)     #Enables CORS for all routes, allows frontend apps (React, etc.) to call this backend

    # -----------------------
    # Config
    # -----------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))    #Gets the absolute path of the app/ directory

    app.config.update(     #Sets multiple Flask configuration values at once
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(BASE_DIR, "app.db"),    #SQLite database stored as app.db inside app/
        SQLALCHEMY_TRACK_MODIFICATIONS=False,   #Disables unnecessary SQLAlchemy tracking
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret"),     #Flask’s internal security key, Uses env value if present, Falls back to "dev-secret" for development
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "dev-jwt-secret"),    #Secret key used to sign JWT tokens
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),    #JWT tokens expire after 30 days
    )

    # -----------------------
    # Init extensions
    # -----------------------
    db.init_app(app)    #Binds SQLAlchemy to this Flask app
    jwt.init_app(app)   #Attaches JWT authentication to the app

    # -----------------------
    # Gemini (ONE place)
    # -----------------------
    gemini_key = os.getenv("GEMINI_API_KEY")    #Reads Gemini API key from environment
    if gemini_key:     #If key exists → configure Gemini
        genai.configure(api_key=gemini_key)    #Authenticates Gemini SDK
        app.gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")   #Creates AI model instance and stores it on app
    else:
        app.gemini_model = None
        print("⚠️ GEMINI_API_KEY not set")     #Safe fallback if key is missing

    # -----------------------
    # Create tables (dev only)
    # -----------------------
    with app.app_context():    #Required for DB operations outside requests
        db.create_all()    #Creates all tables defined in models, runs once at startup

    # -----------------------
    # JWT error handlers
    # -----------------------
    @jwt.expired_token_loader    #Triggered when JWT is valid but expired
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token has expired"}), 401    #Returns clean JSON error response

    @jwt.invalid_token_loader    #Triggered when JWT is malformed or tampered
    def invalid_token_callback(error):
        return jsonify({"msg": f"Invalid token: {error}"}), 422

    @jwt.unauthorized_loader   #Triggered when token is missing
    def missing_token_callback(error):
        return jsonify({"msg": "Authorization token is missing"}), 401

    # -----------------------
    # Request logger (optional)
    # -----------------------
    @app.before_request    #Runs before every request
    def log_request_info():
        if request.path.startswith("/api/"):    #Only logs API requests
            print(f"\n{'='*50}")
            print(f"📥 {request.method} {request.path}")   #Logs HTTP method and path
            if "Authorization" in request.headers:   #Confirms JWT header exists
                print("🔑 Auth header present")
            print(f"{'='*50}\n")

    # -----------------------
    # Register blueprints
    # -----------------------
    app.register_blueprint(main_bp)   #Attaches all route groups to the app so that Flask knows which URLs map to which functions
    app.register_blueprint(auth_bp)
    app.register_blueprint(symptom_bp)
    app.register_blueprint(emergency_chat_bp)

    # -----------------------
    # Health check
    # -----------------------

    
    @app.route("/health")   #Simple endpoint to check system status
    def health():
        return {
            "db": "ok",
            "gemini": bool(app.gemini_model)
        }, 200    #this block confirms that database is reachable and Gemini is loaded

    return app
