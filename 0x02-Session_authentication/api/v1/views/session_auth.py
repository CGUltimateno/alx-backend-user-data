#!/usr/bin/env python3
"""
Module of Session authentication views
"""
import os

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from api.v1.auth.session_auth import SessionAuth


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if email or password is missing
      - 401 if email or password is wrong
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user or not user[0].is_valid_password(password):
        return jsonify({"error": "no user found for this email/password"}), 404
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
