from requests import models, post, status_codes
from typing import Union

from shorty.config import bitly_url, bitly_headers, tinyurl_url

ALLOWED_PROVIDERS = ["bitly", "tinyurl"]

bitly_request_body = {"domain": "bit.ly", "long_url": ""}

tried_providers = []


def shorten_link(request_url: str, request_provider: str) -> Union[int, str]:
    """
    Makes a POST request depending on the url shortening provider given.
    """
    if request_provider not in ALLOWED_PROVIDERS:
        return status_codes.codes.bad_request
    else:
        return _try_shorten_link(request_url, request_provider, tried_providers)


def _try_shorten_link(
    request_url: str, request_provider: str, tried_providers: list
) -> Union[int, str]:
    post_result = provider_post_dict[request_provider](request_url)
    print(post_result)

    if 500 <= post_result.status_code <= 511:
        tried_providers.append(request_provider)
        remaining_providers_list = [
            x for x in ALLOWED_PROVIDERS if x not in tried_providers
        ]
        next_provider = remaining_providers_list[0]
        return _try_shorten_link(request_url, next_provider, tried_providers)
    elif post_result.status_code != status_codes.codes.ok:
        return post_result.status_code
    else:
        return provider_filter_dict[request_provider](post_result)


# Prepares the request body and headers that are intended for the POST request
# and returns either the shortened link or the error status_code.
def _post_to_bitly(request_url: str) -> models.Response:
    bitly_request_body["long_url"] = request_url
    return post(bitly_url, json=bitly_request_body, headers=bitly_headers)


def _post_to_tinyurl(request_url: str) -> models.Response:
    return post(tinyurl_url + request_url)


# Filters the response according to the provider's response
def _filter_from_bitly(response: models.Response) -> str:
    return response.json()["link"]


def _filter_from_tinyurl(response: models.Response) -> str:
    return response.text


provider_post_dict = {"bitly": _post_to_bitly, "tinyurl": _post_to_tinyurl}

provider_filter_dict = {"bitly": _filter_from_bitly, "tinyurl": _filter_from_tinyurl}
