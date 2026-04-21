from flask import Flask, jsonify, request, render_template, Response
from database import init_db, query
from generator import generate_transactions
from scheduler import scheduler
import csv, io

app = Flask(__name__)

# ── Routes ──────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

# KPI summary
@app.route("/api/summary")
def summary():
    rows  = query("SELECT status, COUNT(*) as count, ROUND(SUM(amount),2) as total FROM transactions GROUP BY status")
    total = query("SELECT COUNT(*) as n FROM transactions")[0]["n"]
    return jsonify({"total": total, "by_status": rows})

# Paginated transaction list with filters
@app.route("/api/transactions")
def transactions():
    status   = request.args.get("status", "")
    category = request.args.get("category", "")
    page     = int(request.args.get("page", 1))
    limit    = 50
    where, params = "WHERE 1=1", []
    if status:   where += " AND status=?";   params.append(status)
    if category: where += " AND category=?"; params.append(category)
    rows = query(
        f"SELECT * FROM transactions {where} ORDER BY created_at DESC LIMIT {limit} OFFSET {(page-1)*limit}",
        params
    )
    return jsonify(rows)

# Failure patterns
@app.route("/api/failures")
def failures():
    rows = query("""
        SELECT error_code, gateway, COUNT(*) as count
        FROM transactions
        WHERE status='failed' AND error_code IS NOT NULL
        GROUP BY error_code, gateway
        ORDER BY count DESC
    """)
    return jsonify(rows)

# 30-day trend
@app.route("/api/trend")
def trend():
    rows = query("""
        SELECT DATE(created_at) as day,
               SUM(CASE WHEN status='success' THEN 1 ELSE 0 END) as success,
               SUM(CASE WHEN status='failed'  THEN 1 ELSE 0 END) as failed
        FROM transactions
        WHERE created_at >= DATE('now','-30 days')
        GROUP BY day ORDER BY day
    """)
    return jsonify(rows)

# CSV export
@app.route("/api/export")
def export():
    rows = query("SELECT * FROM transactions ORDER BY created_at DESC")
    buf  = io.StringIO()
    w    = csv.DictWriter(buf, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
    return Response(
        buf.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=transactions.csv"}
    )

# ── Startup ─────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    generate_transactions(5000)
    scheduler.start()
    app.run(debug=True)