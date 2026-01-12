from flask import Blueprint, request, jsonify

# -----------------------
# Try loading Gemini service
# -----------------------
try:
    from app.services.symptom_checker_service import analyze_symptoms_with_gemini
    GEMINI_LOADED = True
except Exception as e:
    print(f"⚠️ Could not load Gemini service: {e}")
    GEMINI_LOADED = False


# -----------------------
# Blueprint
# -----------------------
symptom_bp = Blueprint("symptom", __name__)


# -----------------------
# Routes
# -----------------------

@symptom_bp.route("/api/symptoms/analyze", methods=["POST"])
def analyze_symptoms_route():
    print("✅ --- Request received at /api/symptoms/analyze ---")

    if not GEMINI_LOADED:
        return jsonify({"msg": "Gemini service not available"}), 503

    data = request.get_json() or {}
    symptom_text = data.get("symptoms")

    if not symptom_text:
        print("❌ ERROR: No symptom text provided.")
        return jsonify({"msg": "Symptom text is required"}), 400

    print(f"📄 Symptom received: {symptom_text}")

    try:
        print("🤖 --- Calling Gemini API... ---")
        ai_response = analyze_symptoms_with_gemini(symptom_text)
        print("✅ --- Gemini API call successful! ---")
        return jsonify({"reply": ai_response}), 200

    except Exception as e:
        print(f"❌❌❌ Gemini exception: {e}")
        return jsonify(
            {"msg": "An internal error occurred while analyzing symptoms"}
        ), 500
