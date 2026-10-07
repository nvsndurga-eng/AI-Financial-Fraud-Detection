import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

from utils.database import insert_alert

def send_fraud_email(record):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("ALERT_EMAIL_TO")

    if not all([host, user, password, recipient]):
        msg = "Email alert not sent: SMTP/email environment variables are not configured."
        insert_alert(record["transaction_id"], "EMAIL", "NOT_CONFIGURED", msg, now)
        return {"channel": "EMAIL", "status": "NOT_CONFIGURED", "message": msg}

    email = EmailMessage()
    email["Subject"] = f"Fraud Alert - {record['transaction_id']}"
    email["From"] = user
    email["To"] = recipient
    email.set_content(
        f"""Financial Fraud Detection Alert

Transaction status: {record['prediction']}
Risk score: {record['fraud_probability']}%
Risk level: {record['risk_level']}
Transaction amount: ₹{record['amount']:,.2f}
Transaction type: {record['transaction_type']}
Date/time: {record['timestamp']}

WARNING: The machine-learning system classified this transaction as suspicious.
Please verify the transaction through your normal financial-security process.
"""
    )

    try:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(email)
        status, msg = "SENT", "Email alert sent successfully."
    except Exception as exc:
        status, msg = "FAILED", f"Email alert failed safely: {exc}"

    insert_alert(record["transaction_id"], "EMAIL", status, msg, now)
    return {"channel": "EMAIL", "status": status, "message": msg}
