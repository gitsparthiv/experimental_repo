from flask import Blueprint, request, jsonify
from app.models import Hospital
from app.services.emergency_gemini_service import emergency_ai_response

emergency_chat_bp = Blueprint("emergency_chat", __name__)

@emergency_chat_bp.route("/api/emergency/chat", methods=["POST"])
def emergency_chat():
    data = request.get_json() or {}
    message = data.get("message")

    if not message:
        return jsonify({"msg": "Message required"}), 400

    ai_reply = emergency_ai_response(message)

    hospitals = Hospital.query.all()
    hospital_data = [{
        "name": h.name,
        "distance": h.distance,
        "doctors": h.doctors,
        "beds": h.beds,
        "ventilators": h.ventilators,
        "blood": h.blood
    } for h in hospitals]

    return jsonify({
        "text": ai_reply,
        "hospitals": hospital_data
    }), 200
