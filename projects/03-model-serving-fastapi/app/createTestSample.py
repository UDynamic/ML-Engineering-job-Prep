import pandas as pd
import json

# Load the raw training data
df = pd.read_csv('../data/raw/train.csv')   # adjust path if needed

# Pick the first row (or any row)
sample_row = df.drop('SalePrice', axis=1).iloc[0].to_dict()

# Convert any non-serializable types (e.g., numpy int64) to Python native
sample_json = json.loads(json.dumps(sample_row, default=str))

# Save to a JSON file
with open('testSample.json', 'w') as f:
    json.dump(sample_json, f, indent=2)

print("testSample.json created successfully!")