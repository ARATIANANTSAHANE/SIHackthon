# app.py
from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

# Simple FAQ dataset
faq_data = {
    "what are symptoms of dengue": "Common symptoms include fever, headache, joint pain, and skin rash.",
    "what is covid": "COVID-19 is a viral infection caused by SARS-CoV-2. Symptoms include fever, cough, and difficulty breathing.",
    "vaccination schedule": "Children should receive BCG, DPT, Polio, Hepatitis B, and MMR as per ICMR guidelines.",
    "nearest hospital": "You can visit your district civil hospital or search via Aarogya Setu app."
}

# Basic chatbot logic
def chatbot_response(user_input, lang="en"):
    user_input = user_input.lower()

    # Translate Hindi/other language input to English
    if lang != "en":
        user_input = translator.translate(user_input, src=lang, dest="en").text.lower()

    # Search FAQ
    for key, value in faq_data.items():
        if key in user_input:
            response = value
            break
    else:
        response = "I'm sorry, I don’t have info on that. Please consult a nearby health center."

    # Translate back if query was in Hindi
    if lang != "en":
        response = translator.translate(response, src="en", dest=lang).text

    return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.json["message"]
    lang = request.json.get("lang", "en")
    return jsonify({"response": chatbot_response(user_input, lang)})

if __name__ == "__main__":
    app.run(debug=True)
