#!/usr/bin/python3
"""
API application entry point.
"""

from api.v1.views import app_views
from flask_cors import CORS
import os
from models import storage
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_database_connection(exception):
    """
    Close the database connection at the end of the request.
    """
    storage.close()


@app.errorhandler(400)
def handle_bad_request_error(error):
    """
    Handle bad request errors (HTTP status code 400).
    """
    message = jsonify({"error": error.description})
    return make_response(message, 400)


@app.errorhandler(404)
def handle_not_found_error(error):
    """
    Handle not found errors (HTTP status code 404).
    """
    message = jsonify({"error": "Not found"})
    return make_response(message, 404)


if __name__ == "__main__":
    """
    Get the host and port from environment variables
    Use defaults if not set
    """
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    """
    Run the Flask application
    """
    app.run(host=host, port=port, threaded=True)
