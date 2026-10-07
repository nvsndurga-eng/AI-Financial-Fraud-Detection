# IPD Documentation — AI-Based Financial Fraud Detection System

## 1. Abstract

Financial fraud causes monetary loss and reduces trust in digital transactions.
This project presents an AI/ML-based financial fraud detection system that
accepts transaction attributes, applies a supervised classification model, and
returns a legitimate or suspicious/fraudulent assessment with a probability-based
risk score. The system uses Flask for the web layer, scikit-learn for machine
learning and SQLite for local transaction history. Email and optional SMS alerts
can be triggered for suspicious transactions. Voice input is provided as a
convenience feature, while fingerprint support is explicitly designed as an
integration boundary rather than falsely claiming biometric security.

## 2. Problem Statement

Traditional rule-based fraud systems can struggle with changing transaction
patterns. A data-driven system can learn relationships between transaction
features and known fraud labels and provide an additional automated screening
layer.

## 3. Objectives

- Build a working ML-based fraud classification system.
- Compare suitable classification algorithms.
- Handle class imbalance using class-weighted models and appropriate metrics.
- Provide a simple web interface.
- Store transaction history securely in a local database.
- Generate configurable fraud alerts.
- Provide a student-friendly dashboard and documentation.

## 4. Existing System

Conventional systems may rely heavily on static rules, manual review and fixed
thresholds. Such approaches can generate false positives and may not adapt
quickly to new patterns.

## 5. Proposed System

The proposed system combines transaction preprocessing, supervised machine
learning, risk scoring, local history and configurable notifications in a Flask
application.

## 6. Software Requirements

- Windows 10/11
- Python 3.11+ recommended
- Flask
- pandas
- NumPy
- scikit-learn
- joblib
- python-dotenv
- SQLite
- Modern web browser

## 7. Hardware Requirements

- Dual-core processor or better
- 4 GB RAM minimum; 8 GB recommended
- 1 GB free disk space
- Microphone only if voice input is used
- Supported fingerprint hardware/API only for a real fingerprint integration

## 8. System Architecture

```text
User
  |
  v
Flask Web Interface
  |
  +--> Input Validation
  |
  +--> Trained ML Pipeline
  |       |
  |       +--> Preprocessing
  |       +--> Classifier
  |       +--> Fraud Probability
  |
  +--> Risk Classification
  |
  +--> SQLite Transaction History
  |
  +--> Email Alert
  |
  +--> Optional Twilio SMS
  |
  +--> Optional Voice/Fingerprint integrations
```

## 9. Modules

1. Authentication/Login
2. Transaction Input
3. Machine Learning Prediction
4. Risk Scoring
5. Dashboard
6. Transaction History
7. Alert Center
8. Email Notification
9. SMS Notification
10. Voice Input
11. Fingerprint Integration Boundary
12. Settings
13. Documentation/About

## 10. Methodology

1. Collect or select a documented transaction dataset.
2. Validate required fields.
3. Clean missing/invalid records.
4. Separate features and target.
5. Use a stratified train/test split.
6. Encode transaction type and scale numeric features.
7. Train Logistic Regression and Random Forest.
8. Evaluate with precision, recall, F1 and ROC-AUC in addition to accuracy.
9. Select the model using documented evaluation criteria.
10. Save the trained pipeline.
11. Load it in Flask.
12. Record predictions in SQLite.
13. Trigger optional alerts for fraud predictions.

## 11. Machine Learning Algorithms

### Logistic Regression

A linear probabilistic classifier that models the probability of a binary
outcome. It is useful as a strong baseline and is interpretable compared with
more complex models.

### Random Forest

An ensemble of decision trees. It can model nonlinear relationships and
interactions among transaction features. The implementation uses class weighting
to reduce the impact of class imbalance.

## 12. Class Imbalance

Fraud is often much less common than legitimate activity. Accuracy alone can
therefore be misleading. The training pipeline uses stratified splitting and
class-weighted classifiers. Precision, recall, F1 and ROC-AUC are reported.

## 13. Dataset

The software schema uses amount, transaction type, origin/destination balances
and a binary fraud label. The included demonstration CSV is synthetic and must
not be presented as real-world evidence. For the final IPD report, replace it
with a properly documented public dataset and describe its source, license,
preprocessing and class distribution.

## 14. Flowchart

```text
Start
  |
Login
  |
Enter transaction details
  |
Validate inputs
  |---- Invalid ----> Show error ----> Enter again
  |
Load trained model
  |
Preprocess transaction
  |
Predict class + probability
  |
Determine risk level
  |
Store transaction in SQLite
  |
Fraud?
 /    \
No     Yes
|       |
Show    Send configured
result  email/SMS alerts
 \       /
  Dashboard/history
       |
      End
```

## 15. Advantages

- End-to-end ML pipeline
- Probability/risk output
- Multiple evaluation metrics
- Local database
- Configurable notifications
- Clear separation of optional security integrations
- Runs locally with `python app.py`

## 16. Limitations

- Educational local system, not a banking production system.
- Model quality depends on dataset quality and representativeness.
- Synthetic demo data cannot establish real-world performance.
- Email/SMS depend on third-party services.
- Browser speech input is not biometric authentication.
- Real fingerprint support depends on compatible hardware/API.
- No guarantee of zero false positives or false negatives.

## 17. Future Scope

- Real-time streaming transaction integration
- Explainable AI with feature attribution
- Better calibration of fraud probabilities
- Concept-drift monitoring
- Secure role-based access control
- Production secret management
- Hardware-backed authentication
- Model monitoring and retraining
- Containerized deployment
- Integration with approved financial data sources

## 18. Conclusion

The project demonstrates an end-to-end approach to AI-assisted transaction fraud
screening. It combines supervised machine learning, a web application, local
data persistence and optional alerting. The architecture keeps optional
external/hardware capabilities separate so the core fraud detection system
continues to operate without them.

## 19. References

1. scikit-learn documentation — machine learning algorithms and evaluation.
2. Flask documentation — Python web application framework.
3. Python documentation — standard library.
4. SQLite documentation — embedded relational database.
5. Twilio documentation — programmable messaging API.
6. SpeechRecognition project documentation — speech recognition interfaces.

For the final academic report, add the exact citation for the real dataset and
the papers required by your institution.

## 20. Viva Questions and Answers

### Q1. What is financial fraud detection?
It is the process of identifying transaction patterns that may indicate
unauthorized or deceptive financial activity.

### Q2. Why use machine learning?
Machine learning can learn patterns from labelled historical transactions and
apply those patterns to new transactions.

### Q3. Why is accuracy alone insufficient?
If fraud is rare, a classifier can achieve high accuracy by predicting the
majority legitimate class while still missing many fraudulent transactions.

### Q4. What is precision?
Precision is the fraction of predicted positive cases that are actually positive.

### Q5. What is recall?
Recall is the fraction of actual positive cases that the model successfully
identifies.

### Q6. What is F1-score?
F1 is the harmonic mean of precision and recall.

### Q7. Why Random Forest?
It can model nonlinear relationships and interactions and is relatively robust
for tabular data.

### Q8. Why compare Logistic Regression?
It provides a useful baseline and helps demonstrate whether a more complex model
provides improved evaluation results.

### Q9. What is ROC-AUC?
It summarizes how well a classifier separates the two classes across thresholds.

### Q10. What is class imbalance?
It occurs when one target class has substantially more samples than another.

### Q11. Why use SQLite?
It is lightweight, local and requires no separate database server.

### Q12. Are the probability scores guaranteed to be real-world fraud risk?
No. They are model probabilities based on the training distribution. Calibration
and external validation are needed before interpreting them as real-world risk.

### Q13. Is speech recognition biometric authentication?
No. Speech-to-text identifies spoken words; secure voice biometrics identifies a
speaker using biometric characteristics.

### Q14. Why is fingerprint support marked demo mode?
Hardware access depends on the operating system, sensor and vendor API. The
application must not pretend that unsupported hardware is available.

### Q15. What happens if Twilio is not configured?
The fraud detector continues running and records the SMS alert as
NOT_CONFIGURED instead of crashing.

### Q16. What is Flask?
Flask is a Python web framework used to create the application's routes and
serve the HTML interface.

### Q17. What is the role of train_model.py?
It loads the dataset, preprocesses features, trains and evaluates models, selects
one according to documented metrics, and saves the trained pipeline.

### Q18. Where is the trained model stored?
In `model/fraud_model.pkl`.

### Q19. Where is transaction history stored?
In `database/fraud_detection.db`.

### Q20. How would you improve the project for production?
Use a validated real dataset, stronger authentication, encryption, secure secret
management, monitoring, model calibration, drift detection, audit controls and
appropriate financial/security compliance.
