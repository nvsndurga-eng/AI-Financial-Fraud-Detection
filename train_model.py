"""
Train the financial fraud classifier.

Expected CSV columns:
    amount
    transaction_type
    oldbalanceOrg
    newbalanceOrig
    oldbalanceDest
    newbalanceDest
    isFraud

You can use a real transaction/fraud dataset after mapping its column names to
the schema above. The included demo CSV is explicitly synthetic and is provided
only to verify that the complete software pipeline works end-to-end.
"""

import json
import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_PATH = Path("dataset/transactions.csv")
MODEL_DIR = Path("model")
MODEL_DIR.mkdir(exist_ok=True)

FEATURES = [
    "amount", "transaction_type", "oldbalanceOrg", "newbalanceOrig",
    "oldbalanceDest", "newbalanceDest"
]
TARGET = "isFraud"

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"{DATA_PATH} was not found. Put your CSV there or run "
            f"'python generate_demo_dataset.py' first."
        )
    df = pd.read_csv(DATA_PATH)
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    df = df[FEATURES + [TARGET]].dropna().copy()
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df = df[df[TARGET].isin([0, 1])]
    if df[TARGET].nunique() < 2:
        raise ValueError("The target column must contain both 0 (legitimate) and 1 (fraud).")
    return df

def evaluate(name, estimator, X_train, X_test, y_train, y_test):
    estimator.fit(X_train, y_train)
    pred = estimator.predict(X_test)
    proba = estimator.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "precision": round(precision_score(y_test, pred, zero_division=0), 4),
        "recall": round(recall_score(y_test, pred, zero_division=0), 4),
        "f1": round(f1_score(y_test, pred, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
    }
    print(f"\n{name}")
    print(json.dumps(metrics, indent=2))
    print(classification_report(y_test, pred, zero_division=0))
    return estimator, metrics

def main():
    df = load_data()
    X = df[FEATURES]
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    numeric = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]
    categorical = ["transaction_type"]

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
    ])

    models = {
        "Logistic Regression": Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42))
        ]),
        "Random Forest": Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=300, class_weight="balanced_subsample",
                random_state=42, n_jobs=-1, min_samples_leaf=2
            ))
        ])
    }

    results = {}
    fitted = {}
    for name, estimator in models.items():
        fitted[name], results[name] = evaluate(
            name, estimator, X_train, X_test, y_train, y_test
        )

    # For fraud detection, F1 and recall are important because missing fraud can be costly.
    # We select the model by F1, then ROC-AUC as a tie-breaker.
    selected_name = max(
        results,
        key=lambda n: (results[n]["f1"], results[n]["roc_auc"], results[n]["recall"])
    )
    selected_model = fitted[selected_name]

    joblib.dump(selected_model, MODEL_DIR / "fraud_model.pkl")

    metadata = {
        "selected_model": selected_name,
        "features": FEATURES,
        "target": TARGET,
        "dataset_rows": int(len(df)),
        "fraud_rows": int(y.sum()),
        "legitimate_rows": int((y == 0).sum()),
        "metrics": results,
        "note": "Use a validated real-world fraud dataset for meaningful production evaluation. The included demo dataset is synthetic."
    }
    with open(MODEL_DIR / "model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nSelected model: {selected_name}")
    print(f"Saved: {MODEL_DIR / 'fraud_model.pkl'}")
    print(f"Saved: {MODEL_DIR / 'model_metadata.json'}")

if __name__ == "__main__":
    main()
