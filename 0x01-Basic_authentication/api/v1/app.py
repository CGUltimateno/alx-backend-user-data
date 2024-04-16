#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from api.v1.views import app_views
from flask import jsonify, Flask
from flask_cors import (CORS, cross_origin)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "*"}})
auth = None

auth = os.getenv('AUTH_TYPE')

if auth:
    if auth == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth

        auth = BasicAuth()
    else:
        from api.v1.auth.auth import Auth

        auth = Auth()


@app.errorhandler(404)
def not_found(error):
    """ Error handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def forbidden(error):
    """ Error handler """
    return jsonify({"error": "Forbidden"}), 403
