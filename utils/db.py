"""Direct database assertions for tests."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "test_app.db"

def find_customer_by_email(email):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT id, name, email FROM customers WHERE email = ?", (email,)
        ).fetchone()
    return row
