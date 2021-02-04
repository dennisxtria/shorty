from flask import Blueprint, jsonify, request
from shorty.config import bitly_url, tinyurl_url, generic_access_token


api = Blueprint("api", __name__)

url = [bitly_url, tinyurl_url, generic_access_token]


@api.route("/shortlinks", methods=["POST"])
def create_shortlink():
    return jsonify({})


@api.route("/test", methods=["POST"])
def create_1shortlink():
    return request.get_json()


@api.app_errorhandler(404)
@api.app_errorhandler(405)
@api.app_errorhandler(500)
def _handle_api_error(ex):
    return jsonify(error=str(ex))
