from __future__ import annotations

import os
from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .analysis import analyze_dataset

main = Blueprint("main", __name__)
ALLOWED_EXTENSIONS = {"csv"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@main.route("/upload", methods=["POST"])
def upload_file():
    if "dataset" not in request.files:
        flash("Please choose a CSV file.")
        return redirect(url_for("main.index"))

    file = request.files["dataset"]

    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("main.index"))

    if not _allowed_file(file.filename):
        flash("Only CSV files are supported.")
        return redirect(url_for("main.index"))

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = upload_folder / filename
    file.save(file_path)

    return redirect(url_for("main.dashboard", filename=filename))


@main.route("/dashboard", methods=["GET"])
def dashboard():
    filename = request.args.get("filename", "")
    if not filename:
        flash("Upload a CSV file to view the dashboard.")
        return redirect(url_for("main.index"))

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(file_path):
        flash("File not found. Please upload again.")
        return redirect(url_for("main.index"))

    analysis = analyze_dataset(file_path)
    return render_template("dashboard.html", filename=filename, analysis=analysis)
