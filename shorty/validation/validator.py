from jsonschema import validate
import shorty.validation.schema as schema


class Validator(object):
    def __init__(self, json):
        self.json = json

    def validate(self):
        validate(self.json, schema.SCHEMA)
