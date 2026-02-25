# House Price Prediction API

A production-ready REST API for house price prediction, built with FastAPI and containerized with Docker. The API serves a pre-trained model (scikit-learn/XGBoost pipeline) and provides a `/predict` endpoint that accepts raw house features and returns the predicted sale price.

---

## Project Structure

```
03-model-serving-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── preprocess.py         # Feature engineering and preprocessing logic
│   ├── model.pkl             # Trained model (saved with joblib)
│   └── createTestSample.py   # Helper to generate test JSON from training data
├── requirements.txt          # Python dependencies
├── Dockerfile                 # Docker image definition
├── .dockerignore              # Files to exclude from Docker build
└── README.md                  # This file
```

---

## Requirements

- Python 3.11+
- Docker (optional, for containerized deployment)

---

## Local Setup (without Docker)

1. **Clone the repository** and navigate to the project folder:
   ```bash
   cd projects/03-model-serving-fastapi
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   .\venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API** at `http://localhost:8000`.  
   Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

---

## Running with Docker

1. **Build the Docker image**:
   ```bash
   docker build -t house-price-api .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 --name house-api house-price-api
   ```
   If port 8000 is already in use, change the host port (e.g., `-p 8001:8000`).

3. **Check container logs**:
   ```bash
   docker logs house-api
   ```

4. **Stop and remove the container** when finished:
   ```bash
   docker stop house-api
   docker rm house-api
   ```

---

## API Endpoints

### `GET /` or `GET /health`
Health check endpoint. Returns the status of the API and confirms the model is loaded.

**Response**:
```json
{
  "status": "ok",
  "model_loaded": true
}
```

### `POST /predict`
Accepts raw house features (as JSON) and returns the predicted sale price.

**Request Body**:
A JSON object containing all the features used during training. The exact feature names depend on your dataset (e.g., Ames Housing). Below is an example:

```json
{
  "MSSubClass": 60,
  "MSZoning": "RL",
  "LotFrontage": 65.0,
  "LotArea": 8450,
  "Street": "Pave",
  "Alley": null,
  "LotShape": "Reg",
  "LandContour": "Lvl",
  "Utilities": "AllPub",
  "LotConfig": "Inside",
  "LandSlope": "Gtl",
  "Neighborhood": "CollgCr",
  "Condition1": "Norm",
  "Condition2": "Norm",
  "BldgType": "1Fam",
  "HouseStyle": "2Story",
  "OverallQual": 7,
  "OverallCond": 5,
  "YearBuilt": 2003,
  "YearRemodAdd": 2003,
  "RoofStyle": "Gable",
  "RoofMatl": "CompShg",
  "Exterior1st": "VinylSd",
  "Exterior2nd": "VinylSd",
  "MasVnrType": "BrkFace",
  "MasVnrArea": 196.0,
  "ExterQual": "Gd",
  "ExterCond": "TA",
  "Foundation": "PConc",
  "BsmtQual": "Gd",
  "BsmtCond": "TA",
  "BsmtExposure": "No",
  "BsmtFinType1": "GLQ",
  "BsmtFinSF1": 706,
  "BsmtFinType2": "Unf",
  "BsmtFinSF2": 0,
  "BsmtUnfSF": 150,
  "TotalBsmtSF": 856,
  "Heating": "GasA",
  "HeatingQC": "Ex",
  "CentralAir": "Y",
  "Electrical": "SBrkr",
  "1stFlrSF": 856,
  "2ndFlrSF": 854,
  "LowQualFinSF": 0,
  "GrLivArea": 1710,
  "BsmtFullBath": 1,
  "BsmtHalfBath": 0,
  "FullBath": 2,
  "HalfBath": 1,
  "BedroomAbvGr": 3,
  "KitchenAbvGr": 1,
  "KitchenQual": "Gd",
  "TotRmsAbvGrd": 8,
  "Functional": "Typ",
  "Fireplaces": 0,
  "FireplaceQu": null,
  "GarageType": "Attchd",
  "GarageYrBlt": 2003,
  "GarageFinish": "RFn",
  "GarageCars": 2,
  "GarageArea": 548,
  "GarageQual": "TA",
  "GarageCond": "TA",
  "PavedDrive": "Y",
  "WoodDeckSF": 0,
  "OpenPorchSF": 61,
  "EnclosedPorch": 0,
  "3SsnPorch": 0,
  "ScreenPorch": 0,
  "PoolArea": 0,
  "PoolQC": null,
  "Fence": null,
  "MiscFeature": null,
  "MiscVal": 0,
  "MoSold": 2,
  "YrSold": 2008,
  "SaleType": "WD",
  "SaleCondition": "Normal"
}
```

**Response**:
```json
{
  "price": 208500.0
}
```

If any required feature is missing, the API returns a `400 Bad Request` with details.

---

## Testing the API

### Using `curl`

**Health check**:
```bash
curl http://localhost:8000/health
```

**Prediction** (with a JSON file):
```bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d @testSample.json
```

### Using PowerShell

**Health check**:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**Prediction**:
```powershell
$body = Get-Content testSample.json -Raw
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body -ContentType "application/json"
```

### Generating a Test Sample

If you have the original training data (`train.csv`), you can generate a valid JSON request body by running:

```bash
python app/createTestSample.py
```

This creates a file `testSample.json` containing the first row of the dataset (with the target `SalePrice` removed).

---

## Notes

- The model is loaded with `joblib` at startup, ensuring fast inference.
- Feature engineering (e.g., creating new features) is applied inside the `preprocess.py` module, exactly as done during training.
- All input features must be provided in the request; missing features will result in an error.
- The API is designed to be production‑ready, with proper logging, error handling, and input validation.

---

## License

This project is part of an ML engineering portfolio. Use it as a reference for serving models with FastAPI and Docker.