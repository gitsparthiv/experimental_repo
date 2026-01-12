from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    #print(f"📍 Gemini service loaded: {GEMINI_LOADED}")
    app.run(debug=True, host='0.0.0.0', port=5000)
