# src/train.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from preprocess import preprocessor, engineer_features, numeric_features, categorical_features

# Load data
df = pd.read_csv('../data/raw/train.csv')
X = df.drop('SalePrice', axis=1)
y = df['SalePrice']

# Apply feature engineering
X = engineer_features(X)

# Split into train and validation (hold-out)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.001),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    'XGBoost': xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, n_jobs=-1)
}

cv = KFold(n_splits=5, shuffle=True, random_state=42)
results = {}

for name, model in models.items():
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    
    # Cross-validation
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, 
                                scoring='neg_mean_squared_error')
    rmse_scores = np.sqrt(-cv_scores)
    
    # Fit on full training set
    pipeline.fit(X_train, y_train)
    
    # Validation predictions
    y_pred = pipeline.predict(X_val)
    val_rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    val_r2 = r2_score(y_val, y_pred)
    
    results[name] = {
        'cv_rmse_mean': rmse_scores.mean(),
        'cv_rmse_std': rmse_scores.std(),
        'val_rmse': val_rmse,
        'val_r2': val_r2,
        'pipeline': pipeline
    }
    
    print(f"{name}: CV RMSE = {rmse_scores.mean():.4f} (±{rmse_scores.std():.4f}), "
          f"Val RMSE = {val_rmse:.4f}, R2 = {val_r2:.4f}")
    
# Find best model based on validation RMSE
best_name = min(results, key=lambda x: results[x]['val_rmse'])
best_model = results[best_name]['pipeline']
print(f"\nBest model: {best_name}")

# Save model
joblib.dump(best_model, '../models/final_model.pkl')

# Save results to a text file
with open('../reports/results.txt', 'w') as f:
    for name, res in results.items():
        f.write(f"{name}:\n")
        f.write(f"  CV RMSE: {res['cv_rmse_mean']:.4f} (±{res['cv_rmse_std']:.4f})\n")
        f.write(f"  Validation RMSE: {res['val_rmse']:.4f}\n")
        f.write(f"  Validation R2: {res['val_r2']:.4f}\n\n")
        
# Hyperparameter Tuning
"""
from sklearn.model_selection import GridSearchCV

param_grid = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [3, 5, 7],
    'model__learning_rate': [0.01, 0.1]
}

xgb_pipeline = Pipeline(steps=[('preprocessor', preprocessor), 
                               ('model', xgb.XGBRegressor(random_state=42))])

grid = GridSearchCV(xgb_pipeline, param_grid, cv=cv, scoring='neg_mean_squared_error', n_jobs=-1)
grid.fit(X_train, y_train)

print("Best XGBoost params:", grid.best_params_)
print("Best CV RMSE:", np.sqrt(-grid.best_score_))

# Evaluate on validation
best_xgb = grid.best_estimator_
y_pred = best_xgb.predict(X_val)
val_rmse = np.sqrt(mean_squared_error(y_val, y_pred))
print("Validation RMSE after tuning:", val_rmse)
"""

