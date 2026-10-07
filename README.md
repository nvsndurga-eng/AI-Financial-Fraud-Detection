# Dataset instructions

The application expects `transactions.csv` with:

- amount
- transaction_type
- oldbalanceOrg
- newbalanceOrig
- oldbalanceDest
- newbalanceDest
- isFraud

`isFraud` must use 0 for legitimate and 1 for fraud.

The included CSV is synthetic and is only for software demonstration. For your
final IPD report, use a documented real dataset (for example, an established
public financial fraud dataset), preserve the license/attribution, and document
the exact preprocessing and class distribution.
