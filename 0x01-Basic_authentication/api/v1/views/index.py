#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return stats"""
    from models import storage
    classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
               "reviews": "Review", "states": "State", "users": "User"}
    return jsonify({key: storage.count(value) for key, value in classes.items()})


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized():
    """Return unauthorized"""
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden():
    """Return forbidden"""
    abort(403)
