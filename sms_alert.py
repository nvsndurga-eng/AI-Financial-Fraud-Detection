import os
from datetime import datetime

from utils.database import insert_alert

def send_fraud_sms(record):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    to_number = os.getenv("ALERT_PHONE_TO")

    if not all([sid, token, from_number, to_number]):
        msg = "SMS alert not sent: Twilio environment variables are not configured."
        insert_alert(record["transaction_id"], "SMS", "NOT_CONFIGURED", msg, now)
        return {"channel": "SMS", "status": "NOT_CONFIGURED", "message": msg}

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        body = (
            f"FRAUD ALERT: {record['transaction_id']} | "
            f"Risk {record['fraud_probability']}% ({record['risk_level']}) | "
            f"Amount ₹{record['amount']:,.2f}"
        )
        client.messages.create(body=body, from_=from_number, to=to_number)
        status, msg = "SENT", "SMS alert sent successfully."
    except Exception as exc:
        status, msg = "FAILED", f"SMS alert failed safely: {exc}"

    insert_alert(record["transaction_id"], "SMS", status, msg, now)
    return {"channel": "SMS", "status": status, "message": msg}
