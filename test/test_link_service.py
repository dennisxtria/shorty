from unittest import mock
import unittest
from requests import status_codes
from shorty.service.link_service import shorten_link, _post_to_tinyurl


EXAMPLE_URL = "http://www.example.com/"

INCORRECT_URL = ".example.com/"

INEXISTENT_URL = "http://www.inexistent-key.com/"

UNAVAILABLE_URL = "http://www.unavailable.com/"

EXAMPLE_URL_SHORTENED_WITH_BITLY = "https://bit.ly/3jw6PYF"

EXAMPLE_URL_SHORTENED_WITH_TINYURL = "https://tinyurl.com/d9kp"


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, text, status_code):
            self.json_data = json_data
            self.text = text
            self.status_code = status_code

        def json(self):
            return self.json_data

        def text(self):
            return self.text

        def status_code(self):
            return self.status_code

    if args[0] == "http://tinyurl.com/api-create.php?url=http://www.example.com/":
        return MockResponse(
            {"link": EXAMPLE_URL_SHORTENED_WITH_TINYURL},
            EXAMPLE_URL_SHORTENED_WITH_TINYURL,
            200,
        )
    elif args[0] == "http://tinyurl.com/api-create.php?url=.example.com/":
        return MockResponse("Error", "Error", 400)
    elif (
        args[0] == "https://api-ssl.bitly.com/v4/shorten"
        and kwargs.get("json").get("long_url") == INEXISTENT_URL
    ):
        return MockResponse("Error", "Error", 404)
    elif (
        args[0] == "https://api-ssl.bitly.com/v4/shorten"
        and kwargs.get("json").get("long_url") == UNAVAILABLE_URL
    ):
        return MockResponse(
            {"link": EXAMPLE_URL_SHORTENED_WITH_BITLY},
            EXAMPLE_URL_SHORTENED_WITH_BITLY,
            200,
        )
    elif args[0] == "http://tinyurl.com/api-create.php?url=http://www.unavailable.com/":
        return MockResponse("Error", "Error", 500)


class LinkServiceTestCase(unittest.TestCase):
    @mock.patch("shorty.service.link_service.post", side_effect=mocked_requests_post)
    def test_shorten_link_correct_url_with_tinyurl(self, mock_post):
        url_shortened = shorten_link(EXAMPLE_URL, "tinyurl")

        self.assertEqual(url_shortened, EXAMPLE_URL_SHORTENED_WITH_TINYURL)
        self.assertIn(
            mock.call("http://tinyurl.com/api-create.php?url=http://www.example.com/"),
            mock_post.call_args_list,
        )
        self.assertEqual(len(mock_post.call_args_list), 1)

    @mock.patch("shorty.service.link_service.post", side_effect=mocked_requests_post)
    def test_shorten_link_incorrect_url_with_tinyurl(self, mock_post):
        status_code = shorten_link(INCORRECT_URL, "tinyurl")

        self.assertEqual(status_code, 400)
        self.assertIn(
            mock.call("http://tinyurl.com/api-create.php?url=.example.com/"),
            mock_post.call_args_list,
        )
        self.assertEqual(len(mock_post.call_args_list), 1)

    @mock.patch("shorty.service.link_service.post", side_effect=mocked_requests_post)
    def test_shorten_link_inexistent_key_in_response_with_bitly(self, mock_post):
        status_code = shorten_link(INEXISTENT_URL, "bitly")

        self.assertEqual(status_code, 404)
        self.assertEqual(len(mock_post.call_args_list), 1)

    @mock.patch("shorty.service.link_service.post", side_effect=mocked_requests_post)
    def test_shorten_link_correct_url_with_tinyurl_unavailable(self, mock_post):
        json_data = shorten_link(UNAVAILABLE_URL, "tinyurl")

        self.assertEqual(json_data, EXAMPLE_URL_SHORTENED_WITH_BITLY)
        self.assertIn(
            mock.call(
                "http://tinyurl.com/api-create.php?url=http://www.unavailable.com/"
            ),
            mock_post.call_args_list,
        )
        self.assertEqual(len(mock_post.call_args_list), 2)

    @mock.patch("shorty.service.link_service.post", return_value=200)
    def test_post_to_tinyurl_successful_code_from_tinyurl(self, mock_post):
        response_status_code = _post_to_tinyurl(EXAMPLE_URL)

        assert status_codes.codes.ok == response_status_code
        assert isinstance(response_status_code, int)

    @mock.patch("shorty.service.link_service.post", return_value=400)
    def test__post_to_tinyurl_bad_request_code_from_tinyurl(self, mock_post):
        response_status_code = _post_to_tinyurl(EXAMPLE_URL)

        assert status_codes.codes.bad_request == response_status_code
        assert isinstance(response_status_code, int)

    @mock.patch("shorty.service.link_service.post", return_value=404)
    def test__post_to_tinyurl_not_found_code_from_tinyurl(self, mock_post):
        response_status_code = _post_to_tinyurl(EXAMPLE_URL)

        assert status_codes.codes.not_found == response_status_code
        assert isinstance(response_status_code, int)

    @mock.patch("shorty.service.link_service.post", return_value=500)
    def test__post_to_tinyurl_internal_server_error_code_from_tinyurl(self, mock_post):
        response_status_code = _post_to_tinyurl(EXAMPLE_URL)

        assert status_codes.codes.internal_server_error == response_status_code
        assert isinstance(response_status_code, int)
