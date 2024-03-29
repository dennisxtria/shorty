import logging

from flask import Blueprint, abort, jsonify, request
from jsonschema import ValidationError

from shorty.model.response import Response
from shorty.service.link_service import shorten_link
from shorty.validation.validator import Validator

api = Blueprint("api", __name__)


@api.route("/shortlinks", methods=["POST"])
def create_shortlink():
    """
    Parses and validates the request body and extracts
    the url and provider fields in order to prepare
    the POST request for `link_service.shorten_link()`.

    After that, depending on the type of the result, it is either returned
    with the shortened link, or aborts providing the respective error.
    """
    request_body = request.get_json()

    try:
        logging.info("Validating request body")
        Validator.validate(request_body)
    except ValidationError as e:
        logging.warning(f"Validation failed: {e.message}")
        abort(400, description=e.message)

    request_url = request_body["url"]
    request_provider = request_body.get("provider", "bitly")

    result = shorten_link(request_url, request_provider)

    if isinstance(result, str):
        logging.info(f"{request_url} was successfully shortened to {result}")
        shortened_link_response = Response(url=request_url, link=result).__dict__
        return jsonify(shortened_link_response)
    else:
        abort(result)


@api.app_errorhandler(400)
def bad_request(e):
    """Returns a HTTP 400 error to the Client"""
    return jsonify(error=str(e)), 400


@api.app_errorhandler(403)
def forbidden(e):
    """Returns a HTTP 403 error to the Client"""
    return jsonify(error=str(e)), 403


@api.app_errorhandler(404)
def resource_not_found(e):
    """Returns a HTTP 404 error to the Client"""
    return jsonify(error=str(e)), 404


@api.app_errorhandler(405)
def method_not_allowed(e):
    """Returns a HTTP 405 error to the Client"""
    return jsonify(error=str(e)), 405


@api.app_errorhandler(406)
def not_acceptable(e):
    """Returns a HTTP 406 error to the Client"""
    return jsonify(error=str(e)), 406


@api.app_errorhandler(417)
def expectation_failed(e):
    """Returns a HTTP 417 error to the Client"""
    return jsonify(error=str(e)), 417


@api.app_errorhandler(422)
def unprocessable_entity(e):
    """Returns a HTTP 422 error to the Client"""
    return jsonify(error=str(e)), 422


@api.app_errorhandler(500)
def internal_server_error(e):
    """Returns a HTTP 500 error to the Client"""
    return jsonify(error=str(e)), 500
