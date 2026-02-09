from app import create_app      #Imports create_app() from app/__init__.py

app = create_app()   #This line actually builds your app.

if __name__ == '__main__':   #checks whether the main file is running if true then python run.py
    print("🚀 Starting Flask server...")   #Prints a message to the backend console
    #print(f"📍 Gemini service loaded: {GEMINI_LOADED}")
    app.run(debug=True, host='0.0.0.0', port=5000)   #host: allows access from other devices, If this were 127.0.0.1, only your machine could access it.
