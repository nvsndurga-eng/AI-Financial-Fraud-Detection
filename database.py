import os
import sqlite3
from pathlib import Path

DB_PATH = Path("database/fraud_detection.db")
DB_PATH.parent.mkdir(exist_ok=True)

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE NOT NULL,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            prediction TEXT NOT NULL,
            fraud_probability REAL NOT NULL,
            risk_level TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT NOT NULL,
            channel TEXT NOT NULL,
            status TEXT NOT NULL,
            message TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_transaction(record):
    conn = connect()
    conn.execute("""
        INSERT INTO transactions
        (transaction_id, amount, transaction_type, timestamp, prediction, fraud_probability, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        record["transaction_id"], record["amount"], record["transaction_type"],
        record["timestamp"], record["prediction"], record["fraud_probability"],
        record["risk_level"]
    ))
    conn.commit()
    conn.close()

def insert_alert(transaction_id, channel, status, message, timestamp):
    conn = connect()
    conn.execute(
        "INSERT INTO alerts (transaction_id, channel, status, message, timestamp) VALUES (?, ?, ?, ?, ?)",
        (transaction_id, channel, status, message, timestamp)
    )
    conn.commit()
    conn.close()

def get_transactions(limit=200):
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM transactions ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_alerts(limit=100):
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_stats():
    conn = connect()
    total = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    fraud = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE prediction LIKE 'Fraudulent%'"
    ).fetchone()[0]
    suspicious = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE risk_level = 'MEDIUM'"
    ).fetchone()[0]
    legitimate = total - fraud
    fraud_pct = round((fraud / total) * 100, 2) if total else 0
    conn.close()
    return {
        "total": total,
        "legitimate": legitimate,
        "fraudulent": fraud,
        "suspicious": suspicious,
        "fraud_percentage": fraud_pct
    }

def clear_demo_data():
    conn = connect()
    conn.execute("DELETE FROM alerts")
    conn.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()
