from logging.config import dictConfig

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from shorty.controller.link_controller import api

FLASK_URL = "/api"

SWAGGER_URL = "/api/docs"

API_URL = "/static/swagger.json"

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": __name__}
)


dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                "datefmt": "%Y/%m/%d %H:%M:%S",
            },
            "access": {
                "format": "%(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


def create_app(settings_overrides=None):
    app = Flask(__name__)
    configure_settings(app, settings_overrides)
    configure_blueprints(app)
    return app


def configure_settings(app, settings_override):
    if settings_override:
        app.config.update(settings_override)


def configure_blueprints(app):
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    app.register_blueprint(api, url_prefix=FLASK_URL)
