#!/usr/bin/python3
"""
Module for handling City objects in the API.
"""

from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import jsonify, abort, request, make_response


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
    """
    Retrieves all cities associated with a given state.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    list_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(list_cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """
    Retrieves a city by its ID.
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    Deletes a city by its ID.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Creates a new city within a given state.
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    js = request.get_json()
    obj = City(**js)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Updates a city by its ID.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict())
