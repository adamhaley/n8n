from flask import Flask, request, jsonify, Response, make_response
from openai import OpenAI
import os
from requests_toolbelt.multipart import decoder


app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    
    if request.content_type == "application/octet-stream":
        print("content length header: {}".format(request.content_length))
        data = request.get_data()

        file_stream = request.stream
        filename = request.headers.get('Filename') or 'speech.ogg'
        filepath = os.path.join('./', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        try:
            with open(filepath, 'wb') as file:
                while True:
                    chunk = file_stream.read(4096)
                    if not chunk:
                        break
                    file.write(chunk)
            return Response("File uploaded successfully", status=200)
        except Exception as e:
            # Handle the exception
            error_message = str(e)
            print(f"An error occurred: {error_message}")
            return Response("There was an error: " + error_message,status=500)
    else:
        return jsonify({
            'msg': "415 Unsupported Media Type ;)"
        })

    #audio_file = request.files['body']
    #temp_audio_path = "temp_audio.wav"
    #audio_file.save(temp_audio_path)
    #return jsonify({'success': 'Received audio: ' + request.files['body']})
@app.route('/', methods=['GET'])
def index():
    return 'Listening for audio file on /transcribe'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
