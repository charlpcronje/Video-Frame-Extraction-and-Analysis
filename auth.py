# auth.py - Module for handling API authentication

import json
from flask import request, jsonify

def load_users(file_path='users.json'):
    """
    Load users from a JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def authenticate_api_key(users):
    """
    Authenticate the API key present in the request headers.
    """
    api_key = request.headers.get('API-Key')
    if api_key and api_key in users:
        return True
    return False
