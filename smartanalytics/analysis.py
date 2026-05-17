from __future__ import annotations

import json
from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px


def analyze_dataset(file_path: str) -> dict[str, Any]:
    df = pd.read_csv(file_path)

    if df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "column_names": [],
            "missing_values": {},
            "numeric_summary": {},
            "insights": ["Uploaded CSV is empty."],
            "histogram_html": "",
            "correlation_html": "",
            "preview_rows": [],
        }

    numeric_df = df.select_dtypes(include=[np.number])

    numeric_summary = {}
    if not numeric_df.empty:
        stats_df = numeric_df.describe().round(2)
        numeric_summary = json.loads(stats_df.to_json())

    missing_values = df.isnull().sum().to_dict()
    preview_rows = df.head(10).fillna("").to_dict(orient="records")

    insights = [
        f"Dataset has {len(df)} rows and {len(df.columns)} columns.",
        f"Detected {len(numeric_df.columns)} numeric columns.",
    ]

    if not numeric_df.empty:
        total_missing = int(df.isnull().sum().sum())
        mean_values = numeric_df.mean()
        top_mean_col = mean_values.idxmax() if not mean_values.empty else None

        if top_mean_col:
            insights.append(
                f"Column '{top_mean_col}' has the highest mean ({mean_values[top_mean_col]:.2f})."
            )

        insights.append(f"Total missing values in dataset: {total_missing}.")

    histogram_html = ""
    correlation_html = ""

    if not numeric_df.empty:
        first_numeric_col = numeric_df.columns[0]
        histogram_fig = px.histogram(
            df,
            x=first_numeric_col,
            title=f"Distribution of {first_numeric_col}",
            template="plotly_white",
        )
        histogram_html = histogram_fig.to_html(full_html=False, include_plotlyjs="cdn")

        if len(numeric_df.columns) > 1:
            correlation_fig = px.imshow(
                numeric_df.corr().round(2),
                text_auto=True,
                title="Correlation Matrix",
                color_continuous_scale="Blues",
            )
            correlation_html = correlation_fig.to_html(
                full_html=False, include_plotlyjs=False
            )

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "missing_values": missing_values,
        "numeric_summary": numeric_summary,
        "insights": insights,
        "histogram_html": histogram_html,
        "correlation_html": correlation_html,
        "preview_rows": preview_rows,
    }
