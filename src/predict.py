from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
MODELS_DIR = BASE_DIR / "models"

ID_COL = "ID"
FEATURE_COLUMNS = [
    "crim", "zn", "indus", "chas", "nox", "rm", "age",
    "dis", "rad", "tax", "ptratio", "black", "lstat"
]


def load_model():
    model_path = MODELS_DIR / "model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(
            f"Не найдена модель: {model_path}. Сначала запусти обучение."
        )
    return joblib.load(model_path)


def predict_from_dataframe(df: pd.DataFrame):
    missing = set(FEATURE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Отсутствуют признаки: {sorted(missing)}")

    X = df[FEATURE_COLUMNS]
    model = load_model()
    predictions = model.predict(X)
    return predictions


def predict_test_file():
    test_path = DATA_DIR / "test.csv"
    if not test_path.exists():
        raise FileNotFoundError(f"Не найден файл: {test_path}")

    test_df = pd.read_csv(test_path)
    predictions = predict_from_dataframe(test_df)

    submission = pd.DataFrame({
        ID_COL: test_df[ID_COL],
        "medv": predictions
    })

    output_path = BASE_DIR / "submission.csv"
    submission.to_csv(output_path, index=False)

    print(f"Файл submission сохранён: {output_path}")
    print(submission.head())
    return submission


if __name__ == "__main__":
    predict_test_file()