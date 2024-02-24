#!/usr/bin/python3
"""
View for Amenity objects that handles RESTful API actions.
"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """
    Retrieves all amenities.
    """
    amenities = storage.all(Amenity).values()
    amenities_list = []

    for amenity in amenities:
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """
    Retrieves a specific amenity by ID.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """
    Deletes an amenity by ID.
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """
    Creates a new amenity.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """
    Updates an amenity by ID.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)

    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
