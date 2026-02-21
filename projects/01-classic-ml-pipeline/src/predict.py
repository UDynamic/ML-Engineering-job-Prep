import pandas as pd
import joblib
from preprocess import engineer_features  # reuse same feature engineering

# Load model
model = joblib.load('../models/final_model.pkl')

# Load test data
test = pd.read_csv('../data/raw/test.csv')
test_ids = test['Id']
test = engineer_features(test)  # apply same transformations

# Predict
predictions = model.predict(test)

# Create submission DataFrame
submission = pd.DataFrame({'Id': test_ids, 'SalePrice': predictions})
submission.to_csv('../data/processed/submission.csv', index=False)
print("Predictions saved to ../data/processed/submission.csv")