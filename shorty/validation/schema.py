SCHEMA = {
    "title": "Request",
    "type": "object",
    "properties": {
        "url": {
            "description": "The URL of the request that will be shortened",
            "type": "string",
        },
        "provider": {
            "description": "The provider that will shorten the URL",
            "type": "string",
        },
    },
    "required": ["url"],
}
