# SmartAnalytics – Customer Churn Insights Dashboard

## 📊 Project Overview
This project is a job-ready full-stack analytics app for churn analysis.  
Users upload customer activity CSV data, the Flask backend processes it with Pandas, and a Bootstrap + Chart.js dashboard displays churn insights.

## 🚀 Features
- CSV upload and validation
- Data cleaning + feature engineering (tenure, cohort month, activity month)
- Churn and retention summary metrics
- Cohort analytics and monthly churn trends
- Segment analytics (plan/location when available)
- CSV export for summary reporting

## 🛠️ Tech Stack
- Python 3.x
- Flask
- Pandas
- HTML/CSS/Bootstrap
- JavaScript + Chart.js
- SQLite (optional extension)

## 📁 Key Endpoints
- `POST /api/upload` – upload and process CSV
- `GET /api/summary` – top churn KPIs
- `GET /api/cohorts` – cohort-level churn
- `GET /api/trends` – monthly churn trend
- `GET /api/segments` – plan/location churn segments
- `GET /api/export/summary.csv` – downloadable report

## ▶️ Run Locally
```bash
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## 🧪 Run Tests
```bash
python -m unittest discover -s tests -p "test*.py" -v
```
