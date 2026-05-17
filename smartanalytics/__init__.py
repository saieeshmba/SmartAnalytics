from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "smartanalytics-dev-key"
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

    from .routes import main

    app.register_blueprint(main)
    return app
