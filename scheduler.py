from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3, csv, datetime, os

def generate_daily_report():
    conn = sqlite3.connect("payments.db")
    rows = conn.execute("""
        SELECT category, status, COUNT(*) as count, ROUND(SUM(amount),2) as volume
        FROM transactions
        WHERE DATE(created_at) = DATE('now','-1 day')
        GROUP BY category, status
    """).fetchall()
    conn.close()

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/daily_{datetime.date.today()}.csv"
    with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "status", "count", "volume"])
        w.writerows(rows)
    print(f"✅ Report saved: {filename}")

scheduler = BackgroundScheduler()
scheduler.add_job(generate_daily_report, "cron", hour=0, minute=5)