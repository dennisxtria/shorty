from requests import post, status_codes
from typing import Union

from shorty.config import bitly_url, bitly_headers, tinyurl_url


BITLY_REQUEST_BODY = {"domain": "bit.ly", "long_url": ""}


# Prepares the request body and headers that are intended for the POST request
# and returns either the shortened link or the error status_code.
def _post_to_bitly(request_url: str) -> Union[int, str]:
    BITLY_REQUEST_BODY["long_url"] = request_url
    r = post(bitly_url, json=BITLY_REQUEST_BODY, headers=bitly_headers)

    if r.status_code == status_codes.codes.ok:
        return r.json()["link"]
    else:
        return r.status_code


def _post_to_tinyurl(request_url: str) -> str:
    r = post(tinyurl_url + request_url)
    return r.text


provider_action_dict = {"bitly": _post_to_bitly, "tinyurl": _post_to_tinyurl}


def shorten_link(request_url: str, request_provider: str) -> Union[int, str]:
    """
    Makes a POST request depending on the url shortening provider given.
    """
    return provider_action_dict[request_provider](request_url)
