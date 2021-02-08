from requests import models, post, status_codes
from typing import Union

from shorty.config import bitly_url, bitly_headers, tinyurl_url


BITLY_REQUEST_BODY = {"domain": "bit.ly", "long_url": ""}


# Prepares the request body and headers that are intended for the POST request
# and returns either the shortened link or the error status_code.
def _post_to_bitly(request_url: str) -> models.Response:
    BITLY_REQUEST_BODY["long_url"] = request_url
    return post(bitly_url, json=BITLY_REQUEST_BODY, headers=bitly_headers)


def _post_to_tinyurl(request_url: str) -> models.Response:
    return post(tinyurl_url + request_url)


# Filters the response according to the provider's response
def _filter_from_bitly(response: models.Response) -> str:
    return response.json()["link"]


def _filter_from_tinyurl(response: models.Response) -> str:
    return response.text


provider_post_dict = {"bitly": _post_to_bitly, "tinyurl": _post_to_tinyurl}

provider_filter_dict = {"bitly": _filter_from_bitly, "tinyurl": _filter_from_tinyurl}


def shorten_link(request_url: str, request_provider: str) -> Union[int, str]:
    """
    Makes a POST request depending on the url shortening provider given.
    """
    post_result = provider_post_dict[request_provider](request_url)

    if post_result.status_code != status_codes.codes.ok:
        return post_result.status_code
    else:
        return provider_filter_dict[request_provider](post_result)
