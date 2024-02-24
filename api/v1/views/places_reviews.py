#!/usr/bin/python3
"""
Review endpoints for managing review objects.
"""

from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/places/<place_id>/reviews")
def get_reviews(place_id):
    """
    Retrieve all reviews for a specific place.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    result = []

    for review in place.reviews:
        result.append(review.to_dict())

    return jsonify(result)


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

    review.delete()
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """
    Create a new review for a specific place.
    """
    place = storage.get(Place, place_id)
    payload = request.get_json()

    if not place:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")
    if "user_id" not in payload:
        abort(400, "Missing user_id")
    if not storage.get(User, payload["user_id"]):
        abort(404)
    if "text" not in payload:
        abort(400, "Missing text")

    review = Review(place_id=place_id, **payload)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """
    Update a review by ID.
    """
    review = storage.get(Review, review_id)
    payload = request.get_json()

    if not review:
        abort(404)

    if not payload:
        abort(400, "Not a JSON")

    for key, value in review.to_dict().items():
        if key not in [
            "id",
            "user_id",
            "place_id",
            "created_at",
            "updated_at",
            "__class__",
        ]:
            setattr(review, key, payload[key] if key in payload else value)
    review.save()

    return jsonify(review.to_dict())
