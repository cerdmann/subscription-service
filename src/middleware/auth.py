from functools import wraps
from flask import request, jsonify
import os

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_auth(username, password):
    return (username == os.getenv('API_USERNAME', 'test') and 
            password == os.getenv('API_PASSWORD', 'test123'))

def authenticate():
    return jsonify({'error': 'Authentication required'}), 401