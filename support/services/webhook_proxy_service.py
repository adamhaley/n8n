
from flask import Blueprint, request, Response, abort
import requests
import os

webhook_proxy_bp = Blueprint('webhook_proxy_bp', __name__)

N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')
N8N_API_KEY = os.getenv('N8N_WEBHOOK_KEY')
ALLOWED_DOMAINS = os.getenv('ALLOWED_DOMAINS', '').split(',')

@webhook_proxy_bp.before_request
def limit_remote_addr():
    if request.referrer:
        if not any(domain in request.referrer for domain in ALLOWED_DOMAINS):
            abort(403)
    else:
        abort(403)

@webhook_proxy_bp.route('/webhook/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    if not N8N_WEBHOOK_URL:
        return "N8N_WEBHOOK_URL not configured", 500

    target_url = f"{N8N_WEBHOOK_URL}/{path}"

    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    if N8N_API_KEY:
        headers['X-N8N-API-KEY'] = N8N_API_KEY
    
    try:
        if request.method == 'POST':
            resp = requests.post(target_url, data=request.get_data(), headers=headers, params=request.args)
        else:
            resp = requests.get(target_url, headers=headers, params=request.args)

        response = Response(resp.content, resp.status_code, resp.headers.items())
        return response

    except requests.exceptions.RequestException as e:
        return str(e), 502
