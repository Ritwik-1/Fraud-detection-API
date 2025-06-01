import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, classification_report
from xgboost import XGBClassifier

from imblearn.over_sampling import SMOTE

data_path = "model/synthetic_fraud_dataset.csv"
df = pd.read_csv(data_path)

df.drop_duplicates(inplace=True)
df.drop(columns=["Transaction_ID", "User_ID", "Timestamp"], inplace=True)

binary_cols = ["IP_Address_Flag", "Previous_Fraudulent_Activity", "Is_Weekend"]
df[binary_cols] = df[binary_cols].astype(int)

low_card_cat = ["Transaction_Type", "Card_Type", "Device_Type", "Authentication_Method"]
df = pd.get_dummies(df, columns=low_card_cat, drop_first=True)

df.drop(columns=["Location", "Merchant_Category"], inplace=True)

df["Transaction_Amount"] = np.log1p(df["Transaction_Amount"])
df["Transaction_Distance"] = np.log1p(df["Transaction_Distance"])

features = df.drop("Fraud_Label", axis=1)
scaler = StandardScaler()
df[features.columns] = scaler.fit_transform(features)

X = df.drop("Fraud_Label", axis=1)
y = df["Fraud_Label"]
print("Class distribution before SMOTE:\n", y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

print("Class distribution after SMOTE:\n", pd.Series(y_train_sm).value_counts())

model = XGBClassifier(
    use_label_encoder=False,
    eval_metric="logloss",
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6
)
model.fit(X_train_sm, y_train_sm)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("Classification Report:\n", classification_report(y_test, y_pred))
print(f"ROC AUC: {roc_auc_score(y_test, y_prob):.4f}")

joblib.dump(model, "model/fraud_xgb.pkl")
joblib.dump(scaler, "model/scaler.pkl")
print("Model and scaler saved to model/")
