from pathlib import Path

from flask import Flask


def create_app() -> Flask:
    project_root = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
        static_url_path="/static",
    )
    app.config["SECRET_KEY"] = "smartanalytics-dev-key"
    app.config["UPLOAD_FOLDER"] = str(project_root / "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

    from .routes import main

    app.register_blueprint(main)
    return app
