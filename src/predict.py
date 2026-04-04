import pandas as pd
from pathlib import Path
import joblib

DATA_DIR = Path("../data/raw")
MODEL_DIR = Path("../models")

model = joblib.load(MODEL_DIR / "model.joblib")

test_df = pd.read_csv(DATA_DIR / "test.csv")

ids = test_df["ID"]
X_test = test_df.drop(columns=["ID"])

preds = model.predict(X_test)

submission = pd.DataFrame({
    "ID": ids,
    "medv": preds
})

submission.to_csv("submission.csv", index=False)

print("Submission saved")