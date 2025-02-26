#!/usr/bin/python3
"""
Place API endpoints for managing place objects.
"""

from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from api.v1.views import app_views
from models.amenity import Amenity
from flasgger.utils import swag_from
from flask import jsonify, abort, request, make_response


@app_views.route("/cities/<city_id>/places")
def get_places(city_id):

    """
    Retrieve all places in a specific city.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [obj.to_dict() for obj in city.places]

    return jsonify(places)


@app_views.route("/places/<place_id>")
def get_place(place_id):
    """
    Retrieve a specific place by ID.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """
    Delete a place by ID.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """
    Create a new place in a specific city.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    kwargs = request.get_json()
    kwargs['city_id'] = city_id
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    obj = Place(**kwargs)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """
    Update a place by ID.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())


@app_views.route("/places_search", methods=["POST"])
def search_places():
    """
    Search for places based on specified criteria.
    """
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for place in list_places:
        dict = place.to_dict()
        dict.pop('amenities', None)
        places.append(dict)

    return jsonify(places)
