from flask import Blueprint, request, jsonify
import googleapiclient.discovery
import os

google_search_bp = Blueprint('google_search', __name__)

@google_search_bp.route("/google", methods=["GET"])
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
