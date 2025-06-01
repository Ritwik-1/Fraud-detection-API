import joblib
import numpy as np
import pandas as pd
from app.schemas import TransactionInput

model = joblib.load("model/fraud_xgb.pkl")
scaler = joblib.load("model/scaler.pkl")

OHE_COLUMNS = ["Transaction_Type", "Card_Type", "Device_Type", "Authentication_Method"]
DROP_COLUMNS = ["Transaction_ID", "User_ID", "Timestamp", "Location", "Merchant_Category"]

def preprocess_input(input_data: TransactionInput) -> pd.DataFrame:
    data = pd.DataFrame([input_data.dict()])

    binary_cols = ["IP_Address_Flag", "Previous_Fraudulent_Activity", "Is_Weekend"]
    data[binary_cols] = data[binary_cols].astype(int)

    # Log transform
    data["Transaction_Amount"] = np.log1p(data["Transaction_Amount"])
    data["Transaction_Distance"] = np.log1p(data["Transaction_Distance"])

    # One-hot encoding for known categorical columns
    data = pd.get_dummies(data, columns=OHE_COLUMNS, drop_first=True)

    # Align columns with training
    model_features = model.get_booster().feature_names
    for col in model_features:
        if col not in data.columns:
            data[col] = 0  # add missing columns

    data = data[model_features]  # ensure correct order

    # Scale
    data = pd.DataFrame(scaler.transform(data), columns=data.columns)

    return data

def predict(input_data: TransactionInput) -> str:
    processed = preprocess_input(input_data)
    prediction = model.predict(processed)
    return "fraud" if prediction[0] == 1 else "not fraud"
