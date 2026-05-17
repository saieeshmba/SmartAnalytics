# SmartAnalytics – Full Stack Data Analytics Platform

## 📊 Project Overview
SmartAnalytics is a beginner-friendly full-stack data analytics web app.
Users can upload CSV files, get quick analysis, and view charts in a dashboard.

## 🚀 Features
- Upload CSV datasets
- Data analysis with Pandas and NumPy
- Quick insights (shape, missing values, numeric summary)
- Interactive charts using Plotly
- Simple Flask + HTML/CSS architecture

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Plotly
- **Frontend:** HTML, CSS

## 📁 Clean Folder Structure
```text
SmartAnalytics/
├── app.py
├── requirements.txt
├── Readme.md
├── uploads/
│   └── .gitkeep
├── smartanalytics/
│   ├── __init__.py
│   ├── routes.py
│   └── analysis.py
├── templates/
│   ├── index.html
│   └── dashboard.html
└── static/
    └── css/
        └── styles.css
```

## ✅ Step-by-Step Setup
1. Clone the repository and move into it.
2. Create and activate a virtual environment.
3. Install dependencies from `requirements.txt`.
4. Run the Flask app.
5. Open the app in your browser and upload a CSV file.

### Commands
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows PowerShell

pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:5000`

## 📈 How It Works
1. User uploads a `.csv` file from the upload page.
2. Flask saves the file in `uploads/`.
3. The backend reads data with Pandas.
4. NumPy/Pandas generate basic stats and insights.
5. Plotly creates visualizations for the dashboard.

## 🎯 Goal
Provide a simple, working, and beginner-friendly analytics project that demonstrates full-stack integration with data science workflows.
