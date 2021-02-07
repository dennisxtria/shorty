class Response(object):
    """
    Response model for storing the requested url and shortened link.
    """

    def __init__(self, url: str, link: str):
        self.url = url
        self.link = link
