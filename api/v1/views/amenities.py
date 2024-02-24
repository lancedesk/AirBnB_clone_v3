#!/usr/bin/python3
"""
View for Amenity objects that handles RESTful API actions.
"""

from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """
    Retrieves all amenities.
    """
    amenities = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return make_response(jsonify(amenities_list), 200)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """
    Retrieves a specific amenity by ID.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """
    Deletes an amenity by ID.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"])
def post_amenity():
    """
    Creates a new amenity.
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """
    Updates an amenity by ID.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
