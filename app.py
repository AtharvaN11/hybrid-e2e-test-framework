"""Tiny local demo app used by the automation tests."""
from flask import Flask, jsonify, request, render_template_string
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("test_app.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

PAGE = """
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Demo Customer Portal</title>
<style>
body{font-family:Arial,sans-serif;max-width:850px;margin:40px auto;padding:0 20px;color:#172033}
header{background:#123b52;color:white;padding:22px;border-radius:12px}
table{width:100%;border-collapse:collapse;margin-top:20px}
th,td{text-align:left;padding:12px;border-bottom:1px solid #ddd}
.tag{display:inline-block;background:#dff7e8;color:#17633b;padding:5px 9px;border-radius:20px}
</style></head>
<body>
<header><h1>Customer Portal</h1><p>Local demo application for automated testing</p></header>
<h2>Registered customers</h2>
<p id="customer-count" data-count="{{ customers|length }}">Customers: {{ customers|length }}</p>
<table id="customers-table">
<thead><tr><th>Name</th><th>Email</th></tr></thead>
<tbody>
{% for customer in customers %}
<tr data-email="{{ customer.email }}"><td>{{ customer.name }}</td><td>{{ customer.email }}</td></tr>
{% endfor %}
</tbody></table>
<p class="tag">Demo environment</p>
</body></html>
"""

@app.get("/")
def home():
    with get_connection() as conn:
        customers = conn.execute("SELECT name, email FROM customers ORDER BY id").fetchall()
    return render_template_string(PAGE, customers=customers)

@app.post("/api/customers")
def create_customer():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO customers (name, email) VALUES (?, ?)", (name, email)
            )
            customer_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        return jsonify({"error": "email already exists"}), 409
    return jsonify({"id": customer_id, "name": name, "email": email}), 201

@app.get("/api/customers")
def list_customers():
    with get_connection() as conn:
        rows = conn.execute("SELECT id, name, email FROM customers ORDER BY id").fetchall()
    return jsonify([dict(row) for row in rows])

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
