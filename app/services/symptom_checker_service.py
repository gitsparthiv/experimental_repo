import google.generativeai as genai
import os

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    FORCE_MOCK_MODE = True
else:
    genai.configure(api_key=api_key)


# Try 1.5-flash, fallback to mock if quota issues
FORCE_MOCK_MODE = False  # Set to True to always use mock

try:
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except:
    FORCE_MOCK_MODE = True

def analyze_symptoms_with_gemini(symptom_text: str) -> str:
    # Try real API first
    if not FORCE_MOCK_MODE:
        try:
            prompt = f"""
            You are an empathetic and cautious AI health assistant for NirogNet.
            
            User's symptoms: "{symptom_text}"
            
            Respond naturally with: empathy, clarifying questions, OTC medicine suggestions,
            doctor recommendations, urgency level, and disclaimer.
            """
            
            response = model.generate_content(prompt)
            print("✅ Using real Gemini API")
            return response.text
            
        except Exception as e:
            print(f"⚠️ API failed: {str(e)[:100]}... Falling back to mock response")
            # Falls through to mock response below
    
    # Mock response (professional quality)
    print("🎭 Using intelligent mock response")
    return generate_smart_response(symptom_text)


def generate_smart_response(symptom_text: str) -> str:
    """Professional mock responses based on symptoms"""
    
    symptom_lower = symptom_text.lower()
    
    # Headache
    if 'head' in symptom_lower or 'migraine' in symptom_lower:
        return """I understand you're experiencing a headache. That can be really uncomfortable.

To help you better, could you tell me:
• How severe is the pain on a scale of 1-10?
• How long have you had this headache?
• Are you experiencing any other symptoms like nausea or sensitivity to light?

For immediate relief, you might consider taking Paracetamol (such as Dolo 650 or Crocin) 500-650mg, following the package instructions carefully. Make sure you're not allergic to it. It may also help to rest in a quiet, dark room and stay well hydrated.

I recommend consulting a General Physician or Neurologist if the headache is severe, persists for more than 2-3 days, or if you're experiencing it more frequently than usual. A Neurologist specializes in conditions affecting the brain and nervous system and can properly evaluate your headache.

You can check medicine availability at nearby pharmacies using our Pharmacy Finder feature, or book a video consultation through our app for proper diagnosis.

⚠️ Important: This is preliminary guidance for immediate relief. For accurate diagnosis and treatment, please consult a qualified doctor. In case of sudden, severe headache with vision problems or difficulty speaking, seek immediate medical attention."""

    # Fever
    elif 'fever' in symptom_lower or 'temperature' in symptom_lower:
        return """I'm sorry to hear you have a fever. That must be making you feel quite unwell.

To understand your situation better, could you tell me:
• What is your current temperature?
• How many days have you had the fever?
• Do you have any other symptoms like cough, body aches, or sore throat?

For symptom relief, you might consider Paracetamol (Dolo 650) 650mg every 6-8 hours, following package instructions. Make sure to stay well-hydrated with water, ORS, or coconut water. Get plenty of rest and monitor your temperature.

I recommend consulting a General Physician if the fever persists beyond 3 days, goes above 103°F (39.4°C), or if you develop concerning symptoms. They can determine if you need antibiotics or other treatment.

You can use our app to book a video consultation with a doctor for proper diagnosis and treatment plan.

⚠️ Important: This is preliminary guidance. Please consult a qualified healthcare professional for proper diagnosis and treatment, especially if symptoms worsen or you have underlying health conditions."""

    # Cough/Cold
    elif 'cough' in symptom_lower or 'cold' in symptom_lower or 'throat' in symptom_lower:
        return """I understand you're dealing with cold and cough symptoms. These can be quite bothersome.

To help you better, could you share:
• How long have you had these symptoms?
• Is the cough dry or with phlegm?
• Do you have fever, body aches, or difficulty breathing?

For relief, you might try antihistamines like Cetirizine (follow package instructions), stay well-hydrated with warm fluids like tea or soup, get adequate rest, and use steam inhalation if helpful. Warm salt water gargles can help with throat discomfort.

If symptoms are mild and recent (1-2 days), this could be a common cold which typically resolves on its own in 7-10 days. However, consult a General Physician if symptoms persist beyond a week, you develop high fever, or have difficulty breathing.

Our app's Pharmacy Finder can help you locate nearby pharmacies with these medicines in stock.

⚠️ This is general wellness information. Please consult a qualified healthcare professional for proper diagnosis, especially if you have underlying health conditions or symptoms worsen."""

    # Stomach/digestive
    elif 'stomach' in symptom_lower or 'nausea' in symptom_lower or 'vomit' in symptom_lower or 'diarrhea' in symptom_lower:
        return """I'm sorry to hear you're experiencing stomach issues. That can be very uncomfortable.

To better understand, could you tell me:
• How long have you had these symptoms?
• Is there pain, and if so, where specifically?
• Have you eaten anything unusual recently?

For general stomach discomfort, staying hydrated is crucial. Drink small amounts of water frequently, or try ORS (oral rehydration solution). Avoid spicy, oily foods and stick to bland foods like rice, bananas, or toast. For acidity, antacids like Digene or Eno may provide relief (follow package instructions).

I recommend consulting a General Physician or Gastroenterologist if symptoms persist beyond 24-48 hours, if there's severe pain, blood in stool/vomit, or signs of dehydration. A Gastroenterologist specializes in digestive system disorders.

If symptoms are severe or sudden, please seek immediate medical attention.

⚠️ Important: This is preliminary guidance. For proper diagnosis and treatment, please consult a qualified healthcare professional. In case of severe pain, persistent vomiting, or other concerning symptoms, seek immediate medical care."""

    # Chest pain - URGENT
    elif 'chest' in symptom_lower and 'pain' in symptom_lower:
        return """I understand you're experiencing chest pain. This requires careful attention.

⚠️ IMPORTANT: If you're experiencing severe chest pain, shortness of breath, sweating, or pain radiating to your arm or jaw, please seek IMMEDIATE medical attention by calling emergency services or visiting the nearest emergency room immediately. These could be signs of a serious condition.

If the pain is mild and not accompanied by these symptoms, could you tell me:
• When did the chest pain start?
• Is it sharp, dull, or pressure-like?
• Does it get worse with breathing or movement?

For mild discomfort that may be muscular or due to acidity, avoid physical exertion and rest. However, I strongly recommend consulting a Cardiologist or visiting an Emergency Department as soon as possible. A Cardiologist specializes in heart and cardiovascular conditions and can properly evaluate your chest pain.

Do NOT wait if symptoms worsen. Chest pain should always be evaluated by a medical professional.

⚠️ Disclaimer: Chest pain can have many causes, some serious. Please seek professional medical evaluation immediately. When in doubt, always err on the side of caution and seek emergency care."""

    # Generic response
    else:
        return f"""Thank you for sharing your symptoms: "{symptom_text}". I'm here to help you get appropriate care.

To understand your situation better, could you provide more details:
• How long have you been experiencing these symptoms?
• How severe would you rate them?
• Are there any other symptoms you're noticing?

Based on the information provided, I recommend consulting a healthcare professional who can properly evaluate your symptoms. A General Physician would be a good starting point, and they can refer you to a specialist if needed.

In the meantime, make sure to rest, stay hydrated, and monitor your symptoms. Avoid self-medication without understanding the cause. If symptoms worsen or become severe, please seek immediate medical attention.

You can use our app to:
• Check medicine availability at nearby pharmacies
• Book a video consultation with a doctor
• Get emergency assistance if needed

⚠️ Important: I'm an AI assistant providing general guidance. This is not a medical diagnosis. Please consult a qualified healthcare professional for proper evaluation and treatment. In case of emergency, call your local emergency number immediately."""