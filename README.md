# AI-Based Financial Fraud Detection System

A CSE-DS IPD project built with Python, Flask, scikit-learn and SQLite.

## Important academic note

The included `dataset/transactions.csv` is synthetic and exists only so that the
software can be demonstrated end-to-end. It must not be described as a real
financial dataset or used to claim real-world fraud-detection performance.

For your final academic evaluation, replace it with a documented real fraud
dataset and map the columns to the schema required by `train_model.py`.

## Features

- ML fraud/legitimate classification
- Fraud probability/risk score
- Random Forest + Logistic Regression comparison
- Precision, recall, F1, ROC-AUC and confusion matrix
- SQLite transaction history
- Dashboard
- Email fraud alerts
- Optional Twilio SMS alerts
- Browser speech-input convenience feature
- Optional Python SpeechRecognition availability check
- Fingerprint integration boundary with clearly labelled DEMO MODE
- Environment-variable configuration
- Input validation and error handling

## Windows setup

```powershell
python --version
mkdir AI-Financial-Fraud-Detection
cd AI-Financial-Fraud-Detection
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

If the included demo dataset is absent:

```powershell
python generate_demo_dataset.py
```

Train the model:

```powershell
python train_model.py
```

Copy `.env.example` to `.env` and edit it if you want email/SMS.

Start:

```powershell
python app.py
```

Open:

http://127.0.0.1:5000

Default local login:
- Username: `admin`
- Password: `admin123`

Change these in `.env` before using the application beyond a classroom demo.

## Testing

Use values such as:

### Legitimate-style test
- Amount: 500
- Type: PAYMENT
- Origin old balance: 10000
- Origin new balance: 9500
- Destination old balance: 5000
- Destination new balance: 5500

### High-risk-style test
- Amount: 250000
- Type: TRANSFER
- Origin old balance: 260000
- Origin new balance: 10000
- Destination old balance: 0
- Destination new balance: 250000

The actual result comes from the trained model; these are not hard-coded outcomes.

## Email

For Gmail, use an App Password rather than your normal account password when
2-step verification is enabled. Put the value in `.env`, never in source code.

## SMS

Create a Twilio account, obtain the required credentials/phone numbers, and
place them in `.env`. If they are absent, the fraud detector still works and
records the alert as NOT_CONFIGURED.

## Voice

The browser voice button uses browser speech-recognition support when available.
It is only speech-to-text convenience input. It is NOT biometric authentication.

## Fingerprint

The fingerprint page/status is intentionally a DEMO MODE integration boundary.
Real fingerprint authentication requires supported hardware and a secure
platform/vendor API. The app does not store raw fingerprints.

## Project structure

```text
AI-Financial-Fraud-Detection/
├── app.py
├── train_model.py
├── generate_demo_dataset.py
├── requirements.txt
├── .env.example
├── README.md
├── dataset/
│   └── transactions.csv
├── model/
│   ├── fraud_model.pkl
│   └── model_metadata.json
├── database/
│   └── fraud_detection.db
├── utils/
│   ├── database.py
│   ├── email_alert.py
│   ├── sms_alert.py
│   ├── voice_auth.py
│   └── fingerprint_auth.py
├── templates/
└── static/
```
