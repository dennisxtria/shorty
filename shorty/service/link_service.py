import logging
from typing import Union
from requests import models, post, status_codes
from shorty.config import bitly_url, bitly_headers, tinyurl_url

ALLOWED_PROVIDERS = ["bitly", "tinyurl"]

tried_providers = []


def shorten_link(request_url: str, request_provider: str) -> Union[int, str]:
    """
    Makes a POST request depending on the url shortening provider given.

    In case that a provider is not supported, the response status code is 400.

    Args:
        request_url: the url of the request body that will be shortened.
        request_provider: the desired provider
            with which the url will be shortened.

    Returns:
        The expected return is either a string which represents
        the shortened url or a status code meaning that an error occurred.
    """
    if request_provider not in ALLOWED_PROVIDERS:
        return status_codes.codes.bad_request
    else:
        return _try_shorten_link(request_url, request_provider, tried_providers)


def _try_shorten_link(
    request_url: str, request_provider: str, tried_providers: list
) -> Union[int, str]:
    # The request provider is fetched from a dictionary with the
    # {key: value} being {request_provider: function_post_for_provider}
    # in order to abstract the way the request is posted to each provider.
    #
    # After that, there are 3 possible outcomes:
    # - the url shortening provider has failed to respond, which means that
    #   an server error ranging from 500 to 511 in terms of status code
    #   has occurred, so another request is made to the next
    #   of the remaining provider(s).
    # - the url shortening provider has responsed with an error status code,
    #   so that is returned to the link_controller.
    # - the response of the url provider is fetched in a similar way to the
    #   providers' dictionary, where the shortened link is retrieved from
    #   each provider accordingly.
    logging.info(f"Making POST request to {request_provider}")
    post_result = provider_post_dict[request_provider](request_url)

    if 500 <= post_result.status_code <= 511:
        next_provider = _get_next_provider(request_provider, tried_providers)
        logging.warning(
            f"""Request failed due to server error.
            Retrying with the next available provider: {next_provider}"""
        )
        return _try_shorten_link(request_url, next_provider, tried_providers)
    elif post_result.status_code != status_codes.codes.ok:
        logging.error(f"Unexpected error occurred: {post_result.status_code}")
        return post_result.status_code
    else:
        try:
            return provider_filter_dict[request_provider](post_result)
        except KeyError:
            return status_codes.codes.not_found


def _get_next_provider(request_provider, tried_providers):
    # In case the requested provider was unable to produce a correct response,
    # an iteration through the remaining of the providers takes place.
    try:
        tried_providers.append(request_provider)
        remaining_providers_list = [
            x for x in ALLOWED_PROVIDERS if x not in tried_providers
        ]
        next_provider = remaining_providers_list[0]
        return next_provider
    except IndexError:
        return status_codes.codes.client_closed_request


def _post_to_bitly(request_url: str) -> models.Response:
    # Prepares the request body and headers that are already fetched
    # from the config and are required for the POST request to the bitly API.
    bitly_request_body = {"domain": "bit.ly", "long_url": request_url}
    return post(bitly_url, json=bitly_request_body, headers=bitly_headers)


def _post_to_tinyurl(request_url: str) -> models.Response:
    # Makes a post request which requires only concatenating the requested url
    # to the base url that is intended for the tinyurl API.
    return post(tinyurl_url + request_url)


def _filter_from_bitly(response: models.Response) -> str:
    # Filters the response according to the provider's response body
    # and fetches the shortened url from the respective field.
    #
    # sidenote: This implementation getting the shortened link from the `link`
    # field is specific for this provider, and in case their API changes,
    # future url shortenings should fail with 404 status code to indicate that,
    # and require an appropriate change.
    return response.json()["link"]


def _filter_from_tinyurl(response: models.Response) -> str:
    # Filters the response according to the provider's response
    # and fetches the shortened url from the response.
    return response.text


provider_post_dict = {"bitly": _post_to_bitly, "tinyurl": _post_to_tinyurl}

provider_filter_dict = {"bitly": _filter_from_bitly, "tinyurl": _filter_from_tinyurl}
