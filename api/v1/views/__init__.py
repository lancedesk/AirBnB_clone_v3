#!/usr/bin/python3
"""
This module initializes the blueprint of the API.
"""
from flask import Blueprint

# Import views to register the routes
app_views = Blueprint("app_views", __name__)
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
#from api.v1.views.amenities import *
#from api.v1.views.users import *
#from api.v1.views.places import *
#from api.v1.views.places_reviews import *
