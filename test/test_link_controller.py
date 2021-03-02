class TestLinkController(object):
    def test_create_shortlink_with_correct_request_body(self, client):
        """create_shortlink() with a correct request body
        should respond with a success 200.
        """
        form = {"provider": "tinyurl", "url": "http://example.com"}

        response = client.post("/api/shortlinks", json=form)
        assert response.status_code == 200

    def test_create_shortlink_without_providing_access_token(self, client):
        """create_shortlink() if access_token is not provided to bitly,
        should respond with an error 403.
        """
        form = {"provider": "bitly", "url": "http://example.com"}

        response = client.post("/api/shortlinks", json=form)
        assert response.status_code == 403

    def test_create_shortlink_endpoint_is_wrong(self, client):
        """create_shortlink() if endpoint is wrong,
        should respond with an error 404.
        """
        form = {"provider": "tinyurl", "url": "http://example.com"}

        response = client.post("/api/shortlink", json=form)
        assert response.status_code == 404

    def test_create_shortlink_method_is_not_allowed(self, client):
        """create_shortlink() if method is not allowed,
        should respond with an error 405.
        """
        form = {"provider": "tinyurl", "url": "http://example.com"}

        response = client.get("/api/shortlinks", json=form)
        assert response.status_code == 405

    def test_create_shortlink_provider_is_not_in_valid_format(self, client):
        """create_shortlink() if provider is not in valid format,
        should respond with a validation error 400.
        """
        form = {"provider": 1, "url": "http://example.com"}

        response = client.post("/api/shortlinks", json=form)
        assert response.status_code == 400
