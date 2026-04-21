import sqlite3

def init_db():
    conn = sqlite3.connect("payments.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          TEXT PRIMARY KEY,
            amount      REAL,
            currency    TEXT DEFAULT 'USD',
            status      TEXT,
            category    TEXT,
            gateway     TEXT,
            error_code  TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_status   ON transactions(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON transactions(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_date     ON transactions(created_at)")
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def query(sql, params=()):
    conn = sqlite3.connect("payments.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]