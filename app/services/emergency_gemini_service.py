from flask import current_app
import sys  #Imports Python’s system module

def emergency_ai_response(prompt: str) -> str:  #prompt: str → user’s emergency description (text)  str → AI-generated response or error message
    model = getattr(current_app, "gemini_model", None)  #current_app → the active Flask app , getattr(obj, "attr", None): Tries to get current_app.gemini_model , If it doesn’t exist → returns None

    if not model:   #If the AI model is not loaded or unavailable: Immediately return a safe fallback message, Prevents calling .generate_content() on None
        return "AI service unavailable. Please seek emergency help."

    system_prompt = (     #Sets the role → emergency medical assistant
        "You are an emergency medical assistant.\n"
        "1. Acknowledge the situation.\n"
        "2. Give 3–5 immediate first-aid steps.\n"
        "End with: This is not medical advice."
    )

    try:
        response = model.generate_content(system_prompt + "\nUser: " + prompt)   #Calls the Gemini model, sends system_prompt (instructions), "User: " + actual user emergency message
        return response.text   #Extracts the AI’s text output
    except Exception as e:
        print(e, file=sys.stderr)   #Prints the error message to stderr
        return "AI error. Please call emergency services."
