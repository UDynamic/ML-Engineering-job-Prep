# 🏠 House Prices: Advanced Regression Techniques

An end-to-end machine learning pipeline for predicting house sale prices using the Ames Housing dataset. This project demonstrates a complete workflow: exploratory data analysis (EDA), data preprocessing, feature engineering, model training with cross-validation, and final model selection.

## 📌 Project Overview

- **Goal**: Predict `SalePrice` for residential homes in Ames, Iowa.
- **Dataset**: [House Prices - Advanced Regression Techniques (Kaggle)](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)
- **Task**: Regression
- **Evaluation Metric**: Root Mean Squared Error (RMSE) and R² Score

## 📁 Project Structure
.
├── data/
│   ├── raw/               # Original train.csv and test.csv
│   └── processed/         # Cleaned data / submission files
├── notebooks/
│   └── 01_eda.ipynb       # Exploratory Data Analysis
├── src/
│   ├── __init__.py
│   ├── preprocess.py      # Feature engineering & preprocessing pipelines
│   ├── train.py           # Model training, CV, evaluation
│   └── predict.py         # Generate predictions on test set
├── models/
│   └── final_model.pkl    # Saved best model (joblib)
├── reports/
│   ├── figures/           # Plots from EDA
│   └── results.txt        # Detailed model performance
├── requirements.txt       # Dependencies
└── README.md              # This file

## 📊 Exploratory Data Analysis

The notebook `notebooks/01_eda.ipynb` contains a thorough analysis including:

- Distribution of target variable (`SalePrice`)
- Missing value patterns
- Correlation analysis
- Outlier detection (boxplots, IQR)
- Visualizations saved to `reports/figures/`

**Key Findings**:
- `GrLivArea` and `LotArea` contain extreme values – capped at 4000 and 100,000 respectively.
- Several categorical features (e.g., `Alley`, `PoolQC`) have missing values that indicate absence – treated accordingly.
- Strong positive correlation with `OverallQual`, `GrLivArea`, `GarageCars`, etc.

## ⚙️ Preprocessing & Feature Engineering

All preprocessing steps are encapsulated in `src/preprocess.py` and include:

- **Capping outliers** for `GrLivArea` and `LotArea`
- **Creating new features** (e.g., `TotalSF`, `HouseAge`)
- **Handling missing values**:
  - Numerical: median imputation
  - Categorical: constant "missing" imputation, then one‑hot encoding
- **Scaling** numerical features with `StandardScaler`

A scikit-learn `ColumnTransformer` is used to apply different transformations to numeric and categorical columns, ensuring no data leakage.

## 🤖 Model Training

The script `src/train.py` performs the following:

1. Loads training data and applies feature engineering.
2. Splits data into training (80%) and validation (20%) sets.
3. Defines a 5‑fold cross‑validation strategy.
4. Trains five regression models:
   - Linear Regression
   - Ridge
   - Lasso
   - Random Forest
   - XGBoost
5. Evaluates each using cross‑validation RMSE and validation RMSE / R².
6. Saves the best model (`final_model.pkl`) and a summary of results to `reports/results.txt`.

### Results

| Model               | CV RMSE (mean ± std) | Validation RMSE | R² Score |
|---------------------|----------------------|-----------------|----------|
| Linear Regression   | 32450 ± 2100         | 31500           | 0.85     |
| Ridge               | 31800 ± 1950         | 30900           | 0.86     |
| Lasso               | 33000 ± 2200         | 32100           | 0.84     |
| Random Forest       | 29800 ± 1800         | 28900           | 0.88     |
| XGBoost             | **27500 ± 1500**     | **26800**       | **0.91** |

**Best Model**: XGBoost (further tuned with grid search for optimal hyperparameters).

## 🔮 Making Predictions

To generate predictions on the test set and create a submission file:

```bash
python src/predict.py
```

The output file will be saved as data/processed/submission.csv (format: Id, SalePrice).


## 📈 Future Improvements

- Add more sophisticated feature engineering (e.g., polynomial features, interaction terms).
- Experiment with stacking / ensemble methods.
- Perform Bayesian hyperparameter optimization (e.g., Optuna).
- Build a simple REST API for real‑time predictions.