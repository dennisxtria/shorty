from unittest import mock
import unittest
from requests import status_codes

from shorty.service.link_service import shorten_link, _post_to_tinyurl


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
            {"link": "https://tinyurl.com/d9kp"}, "https://tinyurl.com/d9kp", 200
        )
    elif args[0] == "http://tinyurl.com/api-create.php?url=.example.com/":
        return MockResponse({"link": ".example.com/"}, "Error", 400)
    elif args[0] == "https://api-ssl.bitly.com/v4/shorten":
        return MockResponse(
            {"link": "https://bit.ly/3jw6PYF"}, "https://bit.ly/3jw6PYF", 200
        )
    elif args[0] == "http://tinyurl.com/api-create.php?url=http://www.unavailable.com/":
        return MockResponse("Error", "Error", 500)


class LinkServiceTestCase(unittest.TestCase):
    @mock.patch("shorty.service.link_service.post", side_effect=mocked_requests_post)
    def test_shortening_correct_link_with_tinyurl(self, mock_post):
        json_data = shorten_link("http://www.example.com/", "tinyurl")

        self.assertEqual(json_data, "https://tinyurl.com/d9kp")
        self.assertIn(
            mock.call("http://tinyurl.com/api-create.php?url=http://www.example.com/"),
            mock_post.call_args_list,
        )
        self.assertEqual(len(mock_post.call_args_list), 1)

    @mock.patch("shorty.service.link_service.post", side_effect=mocked_requests_post)
    def test_shortening_incorrect_link_with_tinyurl(self, mock_post):
        status_code = shorten_link(".example.com/", "tinyurl")

        self.assertEqual(status_code, 400)
        self.assertIn(
            mock.call("http://tinyurl.com/api-create.php?url=.example.com/"),
            mock_post.call_args_list,
        )
        self.assertEqual(len(mock_post.call_args_list), 1)

    @mock.patch("shorty.service.link_service.post", side_effect=mocked_requests_post)
    def test_shortening_correct_link_with_tinyurl_unavailable(self, mock_post):
        json_data = shorten_link("http://www.unavailable.com/", "tinyurl")

        self.assertEqual(json_data, "https://bit.ly/3jw6PYF")
        self.assertIn(
            mock.call(
                "http://tinyurl.com/api-create.php?url=http://www.unavailable.com/"
            ),
            mock_post.call_args_list,
        )
        self.assertEqual(len(mock_post.call_args_list), 2)

    @mock.patch("shorty.service.link_service.post", return_value=200)
    def test_getting_successful_code_from_tinyurl(self, mock_post):
        response_status_code = _post_to_tinyurl("http://www.example.com/")

        assert status_codes.codes.ok == response_status_code
        assert isinstance(response_status_code, int)

    @mock.patch("shorty.service.link_service.post", return_value=400)
    def test_getting_bad_request_code_from_tinyurl(self, mock_post):
        response_status_code = _post_to_tinyurl("http://www.example.com/")

        assert status_codes.codes.bad_request == response_status_code
        assert isinstance(response_status_code, int)

    @mock.patch("shorty.service.link_service.post", return_value=404)
    def test_getting_not_found_code_from_tinyurl(self, mock_post):
        response_status_code = _post_to_tinyurl("http://www.example.com/")

        assert status_codes.codes.not_found == response_status_code
        assert isinstance(response_status_code, int)

    @mock.patch("shorty.service.link_service.post", return_value=500)
    def test_getting_internal_server_error_code_from_tinyurl(self, mock_post):
        response_status_code = _post_to_tinyurl("http://www.example.com/")

        assert status_codes.codes.internal_server_error == response_status_code
        assert isinstance(response_status_code, int)
