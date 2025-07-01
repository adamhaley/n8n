from flask import Blueprint, request, jsonify, Response, send_file
import openai
import os
import re
from cartesia import Cartesia
import io

speech_bp = Blueprint('speech', __name__)

@speech_bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if request.content_type == "application/octet-stream":
        print("content length header: {}".format(request.content_length))

        data = request.get_data()
        filename = request.headers.get('Filename') or 'speech.ogg'
        
        try:
            audio_file = io.BytesIO(data)
            audio_file.name = filename # openai expects a file with a name

            transcript = openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format='text'
            )
            transcript_string = ''.join(transcript)

            return jsonify({'msg': transcript_string})
        except Exception as e:
            error_message = str(e)
            print(f"An error occurred: {error_message}")
            return Response("There was an error: " + error_message, status=500)
    else:
        return jsonify({
            'msg': "415 Unsupported Media Type ;)"
        })

@speech_bp.route('/tts', methods=['POST'])
def text_to_speech():
    print("content length header: {}".format(request.content_length))

    client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

    try:
        msg = request.get_data(as_text=True)

        voice_id = os.environ.get("CARTESIA_VOICE_ID")
        voice = client.voices.get(id=voice_id)
        print(voice)
    
        msg = re.sub(r"[^a-zA-Z0-9\s.,!?'():;\-]", "", msg)

        audio_bytes = client.tts.bytes(model_id="sonic-2", transcript=msg, voice={"mode": "id","id": voice_id}, output_format={"container":"mp3","bit_rate":128000,"sample_rate":44100} )
        
        audio_stream = io.BytesIO()
        for chunk in audio_bytes:
            audio_stream.write(chunk)
        audio_stream.seek(0) # Rewind to the beginning of the stream

        return send_file(audio_stream, mimetype="audio/mp3", as_attachment=True, download_name="output.mp3")

    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")
        return Response("There was an error: " + error_message, status=500)
