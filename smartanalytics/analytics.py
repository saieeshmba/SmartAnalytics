from __future__ import annotations

import io

import pandas as pd

REQUIRED_COLUMNS = {"customer_id", "signup_date", "last_activity_date", "status"}
CHURN_STATUSES = {"cancelled", "churned", "inactive"}


class CsvValidationError(ValueError):
    pass


def load_and_clean_csv(file_stream) -> pd.DataFrame:
    df = pd.read_csv(file_stream)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise CsvValidationError(f"Missing required columns: {', '.join(sorted(missing))}")

    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=list(REQUIRED_COLUMNS))
    cleaned["signup_date"] = pd.to_datetime(cleaned["signup_date"], errors="coerce")
    cleaned["last_activity_date"] = pd.to_datetime(cleaned["last_activity_date"], errors="coerce")
    cleaned = cleaned.dropna(subset=["signup_date", "last_activity_date"])
    cleaned["status"] = cleaned["status"].astype(str).str.strip().str.lower()
    cleaned["churned"] = cleaned["status"].isin(CHURN_STATUSES)
    cleaned["tenure_days"] = (cleaned["last_activity_date"] - cleaned["signup_date"]).dt.days.clip(lower=0)
    cleaned["cohort_month"] = cleaned["signup_date"].dt.to_period("M").astype(str)
    cleaned["activity_month"] = cleaned["last_activity_date"].dt.to_period("M").astype(str)
    return cleaned


def build_analytics(df: pd.DataFrame) -> dict:
    total_customers = int(len(df))
    churned_customers = int(df["churned"].sum())
    retained_customers = total_customers - churned_customers
    churn_rate = round((churned_customers / total_customers) * 100, 2) if total_customers else 0.0

    summary = {
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "retained_customers": retained_customers,
        "churn_rate": churn_rate,
        "retention_rate": round(100 - churn_rate, 2),
        "average_tenure_days": round(float(df["tenure_days"].mean()), 2) if total_customers else 0.0,
    }

    cohorts = (
        df.groupby("cohort_month", as_index=False)
        .agg(total_customers=("customer_id", "count"), churned_customers=("churned", "sum"))
        .sort_values("cohort_month")
    )
    cohorts["churn_rate"] = ((cohorts["churned_customers"] / cohorts["total_customers"]) * 100).round(2)

    segments = {}
    for column in ["plan", "location"]:
        if column in df.columns:
            grouped = (
                df.groupby(column, as_index=False)
                .agg(total_customers=("customer_id", "count"), churned_customers=("churned", "sum"))
                .sort_values(column)
            )
            grouped["churn_rate"] = ((grouped["churned_customers"] / grouped["total_customers"]) * 100).round(2)
            segments[column] = grouped.to_dict(orient="records")

    trends = (
        df.groupby("activity_month", as_index=False)
        .agg(total_customers=("customer_id", "count"), churned_customers=("churned", "sum"))
        .sort_values("activity_month")
    )
    trends["churn_rate"] = ((trends["churned_customers"] / trends["total_customers"]) * 100).round(2)

    return {
        "summary": summary,
        "cohorts": cohorts.to_dict(orient="records"),
        "segments": segments,
        "trends": trends.to_dict(orient="records"),
    }


def build_summary_export_csv(analytics: dict) -> str:
    summary_df = pd.DataFrame([analytics["summary"]])
    cohort_df = pd.DataFrame(analytics["cohorts"])
    trend_df = pd.DataFrame(analytics["trends"])

    content = io.StringIO()
    content.write("# Summary\n")
    summary_df.to_csv(content, index=False)
    content.write("\n# Cohorts\n")
    cohort_df.to_csv(content, index=False)
    content.write("\n# Trends\n")
    trend_df.to_csv(content, index=False)

    for segment_name, records in analytics["segments"].items():
        content.write(f"\n# Segment: {segment_name}\n")
        pd.DataFrame(records).to_csv(content, index=False)

    return content.getvalue()
