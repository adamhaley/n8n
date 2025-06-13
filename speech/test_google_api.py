#!/usr/bin/env python3

import os
import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("API_KEY")
cx = os.getenv("CX")

service = googleapiclient.discovery.build("customsearch", "v1", developerKey=api_key)

res = service.cse().list(
    q="where are all the open mics in los angeles?",
    cx=cx
).execute()

print(res)

