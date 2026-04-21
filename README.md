# Payment Analytics Gateway

A full-stack payment analytics platform built with Python, Flask, and SQLite.
Processes 1,000–10,000 test transactions through a real-time monitoring dashboard.

---

## What it does

- Real-time dashboard showing payment success rates and failure patterns
- Cuts manual investigation time from hours to seconds
- Automated daily reporting pipeline — zero manual data extraction
- Drill-down filtering by category, status, gateway, and date

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask |
| Database | SQLite |
| Frontend | HTML, CSS, Chart.js |
| Data Generation | Faker |
| Automation | APScheduler |

---

## Features

- KPI cards — total transactions, success rate, failed volume
- 30-day trend line chart (success vs failed)
- Failure pattern breakdown by error code and gateway
- Transaction table with real-time filters (status, category)
- One-click CSV export
- Automated daily report generation at midnight

---

## Project Structure
---

## How to run locally

**1. Clone the repository**
```bash
git clone https://github.com/YourUsername/payment-analytics.git
cd payment-analytics
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python app.py
```

**4. Open in browser**
http://127.0.0.1:5000
The app auto-generates 10,000 test transactions on first run.

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/summary` | GET | KPI totals by status |
| `/api/transactions` | GET | Paginated transaction list with filters |
| `/api/failures` | GET | Failure pattern breakdown |
| `/api/trend` | GET | 30-day success/fail trend |
| `/api/export` | GET | Download full CSV report |

---

## Key Results

- Processes up to 10,000 transactions with sub-second query response
- Automated reporting pipeline eliminates manual data extraction
- Failure pattern detection surfaces top error codes instantly
