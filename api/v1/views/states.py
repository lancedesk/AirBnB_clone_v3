#!/usr/bin/python3
"""
API routes for managing states.
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route("/states", methods=["GET"])
def get_states():
    """
    Retrieve all states.
    """
    states_list = []
    for state in storage.all("State").values():
        states_list.append(state.to_dict())
    return make_response(jsonify(states_list), 200)


@app_views.route("/states/<string:state_id>", methods=["GET"])
def get_state(state_id):
    """
    Retrieve a specific state by ID.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Delete a state by ID.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"])
def create_state():
    """
    Create a new state.
    """
    if not request.get_json():
        abort(400, "Invalid JSON")
    if "name" not in request.get_json():
        abort(400, "Missing 'name' key in JSON")
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """
    Update an existing state.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Invalid JSON")
    for attr, val in request.get_json().items():
        if attr not in ["id", "created_at", "updated_at"]:
            setattr(state, attr, val)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
