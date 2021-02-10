class Request(object):
    """
    Request model for storing the requested url and shortened link.
    """

    def __init__(self, url: str, provider: str):
        self.url = url
        self.provider = provider
