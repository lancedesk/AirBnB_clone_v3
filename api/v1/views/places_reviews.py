#!/usr/bin/python3
"""
Review endpoints for managing review objects.
"""

from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/places/<string:place_id>/reviews", methods=["GET"])
def get_reviews(place_id):
    """
    Retrieve all reviews for a specific place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return make_response(jsonify(reviews), 200)


@app_views.route("/reviews/<string:review_id>", methods=["GET"])
def get_review(review_id):
    """
    Retrieve a specific review by ID.
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Delete a review by ID.
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """
    Create a new review for a specific place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        abort(400, "Missing user_id")
    user = storage.get("User", kwargs["user_id"])
    if user is None:
        abort(404)
    if "text" not in kwargs:
        abort(400, "Missing text")
    kwargs["place_id"] = place_id
    review = Review(**kwargs)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>", methods=["PUT"])
def update_review(review_id):
    """
    Update a review by ID.
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, val in request.get_json().items():
        if attr not in [
            "id",
            "user_id",
            "place_id",
            "created_at",
            "updated_at",
        ]:
            setattr(review, attr, val)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
