#!/usr/bin/python3
"""
Define routes for API status and statistics.
"""

from models.amenity import Amenity
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.user import User
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/status")
def api_status():

    """
    Retrieve the status of the API.
    Returns:
        dict: A dictionary containing the API status.
    """
    return {"status": "OK"}


@app_views.route("/stats")
def api_stats():
    """
    Retrieve statistics about various models in the database.
    Returns:
    dict: A dictionary containing statistics for each model.
    """
    class_list = [Amenity, City, State, Place, Review, User]
    names = ["amenities", "cities", "states", "places", "reviews", "users"]
    statistics = {}
    for name, cls in zip(names, class_list):
        statistics[name] = storage.count(cls=cls)
    return statistics
