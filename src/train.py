from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
MODELS_DIR = BASE_DIR / "models"

RANDOM_STATE = 42
TARGET_COL = "medv"
ID_COL = "ID"


def rmse_score(y_true, y_pred) -> float:
    mse = mean_squared_error(y_true, y_pred)
    return float(np.sqrt(mse))


def load_training_data() -> pd.DataFrame:
    train_path = DATA_DIR / "train.csv"
    if not train_path.exists():
        raise FileNotFoundError(f"Не найден файл: {train_path}")
    return pd.read_csv(train_path)


def build_features_and_target(df: pd.DataFrame):
    required_columns = {
        "crim", "zn", "indus", "chas", "nox", "rm", "age",
        "dis", "rad", "tax", "ptratio", "black", "lstat",
        TARGET_COL, ID_COL
    }
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"В train.csv отсутствуют колонки: {sorted(missing)}")

    X = df.drop(columns=[TARGET_COL, ID_COL])
    y = df[TARGET_COL]
    return X, y


def train_model():
    df = load_training_data()
    X, y = build_features_and_target(df)

    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_valid)
    rmse = rmse_score(y_valid, y_pred)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / "model.joblib"
    joblib.dump(model, model_path)

    print(f"Модель сохранена в: {model_path}")
    print(f"Validation RMSE: {rmse:.4f}")

    return model, rmse


if __name__ == "__main__":
    train_model()