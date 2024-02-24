#!/usr/bin/python3
"""
Module for handling City objects in the API.
"""

from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
    """
    Retrieves all cities associated with a given state.
    """
    list_cities = []
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """
    Retrieves a city by its ID.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    Deletes a city by its ID.
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Creates a new city within a given state.
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(**data)
    instance.state_id = state.id
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Updates a city by its ID.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
