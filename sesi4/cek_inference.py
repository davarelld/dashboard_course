
# sesi4/cek_inference.py
# Uji inference di terminal sebelum masuk dashboard

import sys
from pathlib import Path

import pandas as pd


pd.set_option("display.width", 140)
pd.set_option("display.max_columns", 20)


ROOT = Path(__file__).resolve().parents[1]

sys.path.append(str(ROOT))


from utils.model_utils import (
    load_model,
    load_metadata,
    validate_input,
    predict
)


# ---------- LOAD METADATA & MODEL ----------

meta = load_metadata()
model = load_model()


# ---------- DISPLAY MODEL INFORMATION ----------

print(
    "Model :",
    type(model).__name__,
    "->",
    [name for name, _ in model.steps]
)

print("Fitur :", meta["feature_order"])


# ---------- LOAD NEW CUSTOMER DATA ----------

baru = pd.read_csv(
    ROOT / "data" / "new_customers.csv"
)


# ---------- VALIDATE INPUT ----------

print(
    "Error validasi:",
    validate_input(baru, meta) or "tidak ada"
)


# ---------- RUN PREDICTION ----------

hasil = predict(model, baru, meta)


# ---------- DISPLAY PREDICTION RESULTS ----------

print(
    hasil[
        [
            "customer_id",
            "contract_type",
            "num_complaints",
            "churn_probability",
            "predicted_churn",
            "risk_category"
        ]
    ].head()
)


# ---------- DISPLAY RISK CATEGORY SUMMARY ----------

print(
    "\nJumlah per kategori risiko:\n",
    hasil["risk_category"].value_counts()
)
