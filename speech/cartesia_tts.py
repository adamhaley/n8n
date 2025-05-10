import requests
from requests_toolbelt.multipart import decoder
from dotenv import load_dotenv
from cartesia import Cartesia

import os

load_dotenv()
# === CONFIGURATION ===
API_URL = "https://api.cartesia.ai/tts"  # Replace with actual endpoint
INPUT_FILE = "scripts/hi_kelly.txt"
OUTPUT_FILE = "output.mp3"               # Or output.wav depending on API response

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))
voice_id = os.environ.get("CARTESIA_VOICE_ID")

voice = client.voices.get(id=voice_id)

try:

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        msg = f.read()
    
    audio_bytes = client.tts.bytes(model_id="sonic-2", transcript=msg, voice={"mode": "id","id": voice_id}, output_format={"container":"mp3","bit_rate":128000,"sample_rate":44100} )

    with open(OUTPUT_FILE, "wb") as f:
        for chunk in audio_bytes:
            f.write(chunk)
        f.close()

        print(f"Audio saved to {OUTPUT_FILE}")

except Exception as e:
    error_message = str(e)
    print(f"An error occurred: {error_message}")

