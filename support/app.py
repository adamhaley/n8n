from flask import Flask, request, jsonify, Response
import os
from dotenv import load_dotenv

from services.speech_service import speech_bp
from services.name_generator_service import name_generator_bp
from services.google_search_service import google_search_bp

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    print("Warning: OPENAI_API_KEY not set. Some services may not function correctly.")

app = Flask(__name__)

app.register_blueprint(speech_bp)
app.register_blueprint(name_generator_bp)
app.register_blueprint(google_search_bp)

@app.route('/', methods=['GET'])
def index():
    return 'n8n Workflow Support Server is running.'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)