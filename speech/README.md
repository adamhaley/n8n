python -m venv venv

pip3 install -r requirements.txt

#transcribe:


#tts

curl -H 'Content-Type: application/json' \
      -d '{ "title":"foo","body":"bar", "id": 1}' \
      -X POST \
      http://192.168.1.9:8000/
