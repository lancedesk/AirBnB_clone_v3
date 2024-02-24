#!/usr/bin/python3
"""
Module for handling City objects in the API.
"""

from models import storage
from models.city import City
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
    """
    Retrieves all cities associated with a given state.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return make_response(jsonify(cities), 200)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """
    Retrieves a city by its ID.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    Deletes a city by its ID.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Creates a new city within a given state.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    city = City(**request.json)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Updates a city by its ID.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
