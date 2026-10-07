import os
import uuid
from datetime import datetime, timezone
from functools import wraps

import joblib
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from utils.database import (
    init_db, insert_transaction, get_transactions, get_stats, get_alerts,
    clear_demo_data
)
from utils.email_alert import send_fraud_email
from utils.sms_alert import send_fraud_sms
from utils.voice_auth import voice_status
from utils.fingerprint_auth import fingerprint_status

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-development-secret")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

MODEL_PATH = os.path.join("model", "fraud_model.pkl")
METADATA_PATH = os.path.join("model", "model_metadata.json")
model = None
metadata = {}

def load_model():
    global model, metadata
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    if os.path.exists(METADATA_PATH):
        import json
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)

load_model()
init_db()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        # This is a local student-project login. It is not intended for production.
        expected_user = os.getenv("APP_USERNAME", "admin")
        expected_password = os.getenv("APP_PASSWORD", "admin123")
        if username == expected_user and request.form.get("password", "") == expected_password:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    stats = get_stats()
    recent = get_transactions(limit=8)
    return render_template("dashboard.html", stats=stats, recent=recent, metadata=metadata)

@app.route("/detect", methods=["GET", "POST"])
@login_required
def detect():
    result = None
    form = {}
    if request.method == "POST":
        if model is None:
            flash("No trained model found. Run: python train_model.py", "danger")
            return render_template("detect.html", result=None, form=request.form)

        form = request.form.to_dict()
        try:
            amount = float(form.get("amount", ""))
            oldbalance_org = float(form.get("oldbalanceOrg", ""))
            newbalance_orig = float(form.get("newbalanceOrig", ""))
            oldbalance_dest = float(form.get("oldbalanceDest", ""))
            newbalance_dest = float(form.get("newbalanceDest", ""))
            transaction_type = form.get("transaction_type", "").strip()

            if amount < 0 or min(oldbalance_org, newbalance_orig, oldbalance_dest, newbalance_dest) < 0:
                raise ValueError("Amounts and balances cannot be negative.")
            if not transaction_type:
                raise ValueError("Transaction type is required.")

            row = pd.DataFrame([{
                "amount": amount,
                "transaction_type": transaction_type,
                "oldbalanceOrg": oldbalance_org,
                "newbalanceOrig": newbalance_orig,
                "oldbalanceDest": oldbalance_dest,
                "newbalanceDest": newbalance_dest
            }])

            prediction = int(model.predict(row)[0])
            probabilities = model.predict_proba(row)[0]
            classes = list(model.classes_)
            fraud_probability = float(probabilities[classes.index(1)]) if 1 in classes else 0.0

            if fraud_probability >= 0.80:
                risk = "HIGH"
            elif fraud_probability >= 0.50:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            status = "Fraudulent / Suspicious" if prediction == 1 else "Genuine / Legitimate"
            transaction_id = "TX-" + uuid.uuid4().hex[:10].upper()
            timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")

            record = {
                "transaction_id": transaction_id,
                "amount": amount,
                "transaction_type": transaction_type,
                "timestamp": timestamp,
                "prediction": status,
                "fraud_probability": round(fraud_probability * 100, 2),
                "risk_level": risk
            }
            insert_transaction(record)

            alerts = []
            if prediction == 1:
                email_result = send_fraud_email(record)
                sms_result = send_fraud_sms(record)
                alerts = [email_result, sms_result]

            result = {**record, "alerts": alerts}
        except ValueError as exc:
            flash(str(exc), "danger")
        except Exception as exc:
            app.logger.exception("Prediction error")
            flash(f"Prediction failed safely: {exc}", "danger")

    return render_template("detect.html", result=result, form=form)

@app.route("/history")
@login_required
def history():
    transactions = get_transactions(limit=200)
    return render_template("history.html", transactions=transactions)

@app.route("/alerts")
@login_required
def alerts():
    return render_template("alerts.html", alerts=get_alerts())

@app.route("/settings")
@login_required
def settings():
    return render_template(
        "settings.html",
        voice=voice_status(),
        fingerprint=fingerprint_status(),
        email_enabled=bool(os.getenv("SMTP_HOST") and os.getenv("ALERT_EMAIL_TO")),
        sms_enabled=bool(os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN") and os.getenv("TWILIO_FROM_NUMBER") and os.getenv("ALERT_PHONE_TO"))
    )

@app.route("/about")
@login_required
def about():
    return render_template("about.html", metadata=metadata)

@app.route("/api/stats")
@login_required
def api_stats():
    return jsonify(get_stats())

@app.route("/demo/reset", methods=["POST"])
@login_required
def reset_demo():
    clear_demo_data()
    flash("Local transaction history cleared.", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    # Debug is off by default for safer local use.
    app.run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG", "0") == "1")
