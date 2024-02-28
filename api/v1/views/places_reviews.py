#!/usr/bin/python3
"""
Review endpoints for managing review objects.
"""

from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request


@app_views.route("/places/<place_id>/reviews")
def get_reviews(place_id):

    """
    Retrieve all reviews for a specific place.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route("/reviews/<review_id>")
def get_review(review_id):
    """
    Retrieve a specific review by ID.
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Delete a review by ID.
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """
    Create a new review for a specific place.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """
    Update a review by ID.
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
