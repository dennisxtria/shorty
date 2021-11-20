from jsonschema import validate

import shorty.validation.schema as schema


class Validator(object):
    """
    Validator model for ensuring the type of the provided fields
    based on the provided JSON schema.
    """

    def __init__(self, json):
        self.json = json

    def validate(self):
        validate(self, schema.SCHEMA)
