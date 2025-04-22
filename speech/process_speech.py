from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    temp_audio_path = "temp_audio.wav"
    audio_file.save(temp_audio_path)

@app.route('/', methods=['GET'])
def index():
    return 'Listening for audio file on /transcribe'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
