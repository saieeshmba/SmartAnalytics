import io

from flask import Blueprint, current_app, jsonify, render_template, request, send_file

from .analytics import CsvValidationError, REQUIRED_COLUMNS, build_analytics, build_summary_export_csv, load_and_clean_csv


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/")
def index():
    return render_template("index.html")


def _require_analytics():
    analytics = current_app.config.get("ANALYTICS_CACHE")
    if not analytics:
        return None, (jsonify({"error": "No dataset uploaded yet."}), 400)
    return analytics, None


@dashboard_bp.post("/api/upload")
def upload_file():
    uploaded_file = request.files.get("file")
    if not uploaded_file or not uploaded_file.filename:
        return jsonify({"error": "Please upload a CSV file."}), 400
    if not uploaded_file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are supported."}), 400

    try:
        dataframe = load_and_clean_csv(uploaded_file)
    except CsvValidationError:
        required = ", ".join(sorted(REQUIRED_COLUMNS))
        return jsonify({"error": f"Missing required columns. Required columns: {required}."}), 400
    except Exception:
        return jsonify({"error": "Unable to process file. Ensure it is a valid CSV."}), 400

    if dataframe.empty:
        return jsonify({"error": "Dataset is empty after validation and cleaning."}), 400

    analytics = build_analytics(dataframe)
    current_app.config["PROCESSED_DATA"] = dataframe
    current_app.config["ANALYTICS_CACHE"] = analytics

    return jsonify({"message": "Upload successful.", "summary": analytics["summary"]})


@dashboard_bp.get("/api/summary")
def get_summary():
    analytics, error = _require_analytics()
    if error:
        return error
    return jsonify(analytics["summary"])


@dashboard_bp.get("/api/cohorts")
def get_cohorts():
    analytics, error = _require_analytics()
    if error:
        return error
    return jsonify(analytics["cohorts"])


@dashboard_bp.get("/api/segments")
def get_segments():
    analytics, error = _require_analytics()
    if error:
        return error
    return jsonify(analytics["segments"])


@dashboard_bp.get("/api/trends")
def get_trends():
    analytics, error = _require_analytics()
    if error:
        return error
    return jsonify(analytics["trends"])


@dashboard_bp.get("/api/export/summary.csv")
def export_summary_csv():
    analytics, error = _require_analytics()
    if error:
        return error

    csv_content = build_summary_export_csv(analytics)
    return send_file(
        io.BytesIO(csv_content.encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="customer_churn_summary.csv",
    )
