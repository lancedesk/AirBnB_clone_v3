#!/usr/bin/python3
"""
API routes for managing states.
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import jsonify, abort, request, make_response


@app_views.route("/states", methods=["GET"])
def get_states():
    """
    Retrieve all states.
    """
    states_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route("/states/<string:state_id>", methods=["GET"])
def get_state(state_id):
    """
    Retrieve a specific state by ID.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Delete a state by ID.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"])
def create_state():
    """
    Create a new state.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    obj = State(**js)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """
    Update an existing state.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
