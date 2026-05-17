import os
import secrets
from pathlib import Path

from flask import Flask

from .routes import dashboard_bp


def create_app(test_config=None):
    project_root = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    app.config.update(
        SECRET_KEY=os.environ.get("SMARTANALYTICS_SECRET_KEY", secrets.token_hex(32)),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
        PROCESSED_DATA=None,
        ANALYTICS_CACHE=None,
    )

    if test_config:
        app.config.update(test_config)

    app.register_blueprint(dashboard_bp)
    return app
