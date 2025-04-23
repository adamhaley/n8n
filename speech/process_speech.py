from flask import Flask, request, jsonify, Response, make_response
import openai
import os
import json
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

@app.route('/', methods=['GET'])
def index():
    return 'Listening for audio file on /transcribe'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
