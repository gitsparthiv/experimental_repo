from flask import current_app
import sys

def emergency_ai_response(prompt: str) -> str:
    model = getattr(current_app, "gemini_model", None)

    if not model:
        return "AI service unavailable. Please seek emergency help."

    system_prompt = (
        "You are an emergency medical assistant.\n"
        "1. Acknowledge the situation.\n"
        "2. Give 3–5 immediate first-aid steps.\n"
        "End with: This is not medical advice."
    )

    try:
        response = model.generate_content(system_prompt + "\nUser: " + prompt)
        return response.text
    except Exception as e:
        print(e, file=sys.stderr)
        return "AI error. Please call emergency services."
