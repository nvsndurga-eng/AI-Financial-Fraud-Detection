"""
Generate a transparent synthetic dataset ONLY for testing the software pipeline.

This is not a substitute for a real fraud dataset and must not be presented as
real-world model performance in an academic report.
"""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 6000
types = rng.choice(["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"], size=n,
                   p=[0.40, 0.22, 0.20, 0.08, 0.10])

amount = np.round(rng.lognormal(mean=7.0, sigma=1.0, size=n), 2)
old_org = np.round(rng.uniform(0, 300000, size=n), 2)
new_orig = np.maximum(old_org - amount, 0)
old_dest = np.round(rng.uniform(0, 500000, size=n), 2)
new_dest = old_dest + amount

# Transparent synthetic signal used only so the included demo model has learnable labels.
score = (
    (amount > 180000).astype(int) * 2.0
    + ((types == "TRANSFER") | (types == "CASH_OUT")).astype(int) * 1.2
    + ((old_org > 0) & (new_orig < old_org * 0.15)).astype(int) * 1.5
    + ((old_dest == 0) & (types == "TRANSFER")).astype(int) * 0.8
    + rng.normal(0, 0.9, n)
)
prob = 1 / (1 + np.exp(-(score - 3.0)))
is_fraud = (rng.random(n) < prob * 0.65).astype(int)

df = pd.DataFrame({
    "amount": amount,
    "transaction_type": types,
    "oldbalanceOrg": old_org,
    "newbalanceOrig": new_orig,
    "oldbalanceDest": old_dest,
    "newbalanceDest": new_dest,
    "isFraud": is_fraud
})

out = Path("dataset/transactions.csv")
out.parent.mkdir(exist_ok=True)
df.to_csv(out, index=False)
print(f"Created {out} with {len(df)} rows.")
print("IMPORTANT: This dataset is synthetic and is only for software/demo testing.")
