from flask import Blueprint, jsonify, request, abort
from jsonschema import ValidationError
from requests import post
from shorty.config import bitly_url, bitly_headers, tinyurl_url
from shorty.model.response import Response
from shorty.validation.validator import Validator


api = Blueprint("api", __name__)

BITLY_REQUEST_BODY = {"domain": "bit.ly", "long_url": ""}


def _post_to_bitly(request_url: str):
    BITLY_REQUEST_BODY["long_url"] = request_url
    r = post(bitly_url, json=BITLY_REQUEST_BODY, headers=bitly_headers)
    return r.json()["link"]


def _post_to_tinyurl(request_url: str):
    r = post(tinyurl_url + request_url)
    return r.text


provider_action_dict = {"bitly": _post_to_bitly, "tinyurl": _post_to_tinyurl}


@api.route("/shortlinks", methods=["POST"])
def create_shortlink():
    request_body = request.get_json()

    try:
        Validator.validate(request_body)
    except ValidationError as e:
        abort(500, description=e.message)

    request_url = request_body["url"]
    request_provider = request_body.get("provider", "bitly")

    if request_provider not in provider_action_dict:
        abort(404, description="The requested URL shortening provider was not found.")

    shortened_link = provider_action_dict[request_provider](request_url)

    return jsonify(Response(url=request_url, link=shortened_link).__dict__)


@api.app_errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@api.app_errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@api.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify(error=str(e)), 405


@api.app_errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500
