from flask import Flask, request, jsonify, Response, make_response
import openai
import os
import json
import re
import random
import googleapiclient.discovery
from requests_toolbelt.multipart import decoder
from dotenv import load_dotenv
    
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    
    if request.content_type == "application/octet-stream":
        print("content length header: {}".format(request.content_length))


        data = request.get_data()
        filename = request.headers.get('Filename') or 'speech.ogg'
        filepath = os.path.join('./', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        try:
            with open(filepath, 'wb') as file:
                file.write(data)
                file.close()

                audio_file = open(filepath, "rb")
                
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    response_format='text'
                )
                transcript_string = ''.join(transcript)

            return jsonify({'msg': transcript_string})
        except Exception as e:
            # Handle the exception
            error_message = str(e)
            print(f"An error occurred: {error_message}")
            return Response("There was an error: " + error_message,status=500)

        return jsonify({
            'msg': "received data ;)"
            })
    else:
        return jsonify({
            'msg': "415 Unsupported Media Type ;)"
        })

@app.route('/tts', methods=['POST'])
def text_to_speech():
    print("content length header: {}".format(request.content_length))

    from flask import send_file
    from cartesia import Cartesia
    
    client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

    try:
        msg = request.get_data(as_text=True)

        voice_id = os.environ.get("CARTESIA_VOICE_ID")
        voice = client.voices.get(id=voice_id)
        print(voice)

        file_path = "output.wav"
    
        msg = re.sub(r"[^a-zA-Z0-9\s.,!?\"'():;\-]", "", msg)

        audio_bytes = client.tts.bytes(model_id="sonic-2", transcript=msg, voice={"mode": "id","id": voice_id}, output_format={"container":"mp3","bit_rate":128000,"sample_rate":44100} )
        with open(file_path, "wb") as f:
            for chunk in audio_bytes:
                f.write(chunk)
            f.close()
        try:
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return f"Error sending file: {str(e)}", 500

    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")
        return Response("There was an error: " + error_message,status=500)
    
    return jsonify({
            'msg': "wrote file ;)"
            })

    
    return jsonify({
            'msg': "wrote file ;)"
            })

    #data = request.get_data()
    #return jsonify(data)
    
@app.route("/generate-name", methods=["GET"])
def generate_name():
    adjectives = [
        "quick", "bright", "silent", "brave", "calm", "lucky", "sunny", "clever", "happy", "shiny"
    ]
    nouns = [
        "tiger", "hill", "cloud", "river", "falcon", "stone", "tree", "flame", "wave", "trail"
    ]

    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = str(random.randint(0, 9999)).zfill(4)

    return f"{adjective}-{noun}-{number}"

    return jsonify({"name": name})

@app.route("/google", methods=["GET"])
def google_search():
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("CX")

    service = googleapiclient.discovery.build("customsearch", "v1", developerKey=api_key)

    query = request.args.get('q')

    if query:
        res = service.cse().list(
            q=query,
            cx=cx
        ).execute()

        return jsonify({"name": res})
    else:
        return "No search query provided"


@app.route('/', methods=['GET'])
def index():
    return 'Listening for audio file on /transcribe'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
