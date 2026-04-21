from faker import Faker
import sqlite3, uuid, random

fake = Faker()

CATEGORIES  = ["retail", "subscription", "refund", "marketplace"]
GATEWAYS    = ["stripe", "paypal", "razorpay", "square"]
ERROR_CODES = ["card_declined", "insufficient_funds", "expired_card", "network_timeout"]

def generate_transactions(count=5000):
    conn = sqlite3.connect("payments.db")
    rows = []
    for _ in range(count):
        status = random.choices(["success", "failed", "pending"], weights=[75, 20, 5])[0]
        error  = random.choice(ERROR_CODES) if status == "failed" else None
        rows.append((
            str(uuid.uuid4()),
            round(random.uniform(5, 2000), 2),
            "USD",
            status,
            random.choice(CATEGORIES),
            random.choice(GATEWAYS),
            error,
            fake.date_time_between(start_date="-30d").isoformat()
        ))
    conn.executemany(
        "INSERT OR IGNORE INTO transactions VALUES (?,?,?,?,?,?,?,?)", rows
    )
    conn.commit()
    conn.close()
    print(f"✅ {count} transactions inserted successfully.")