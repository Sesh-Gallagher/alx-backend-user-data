#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from os import getenv

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = os.getenv('AUTH_TYPE')


def get_auth():
    """
    Module all auth classes getter
    """
    from api.v1.auth.auth import Auth
    from api.v1.auth.basic_auth import BasicAuth
    from api.v1.auth.session_auth import SessionAuth
    from api.v1.auth.session_exp_auth import SessionExpAuth
    from api.v1.auth.session_db_auth import SessionDBAuth

    authentication_repo = {
        'auth': Auth,
        'basic_auth': BasicAuth,
        'session_auth': SessionAuth,
        'session_exp_auth': SessionExpAuth,
        'session_db_auth': SessionDBAuth
    }

    return authentication_repo


if auth:
    try:
        auth = get_auth()[auth]()
    except Exception:
        auth = None


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Represents not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """
    Represents unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """
    Represents forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> None:
    """
    Represents filter for request
    """
    request_path_list = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/']
    if auth:
        if auth.require_auth(request.path, request_path_list):
            if auth.authorization_header(
                    request) is None and auth.session_cookie(request) is None:
                abort(401)
            request.current_user = auth.current_user(request)
            if auth.current_user(request) is None:
                abort(403)
            if request.current_user is None:
                abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
