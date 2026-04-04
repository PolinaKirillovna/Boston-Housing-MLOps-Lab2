import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Пути
DATA_DIR = Path("../data/raw")
MODEL_DIR = Path("../models")

MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Загрузка данных
train_df = pd.read_csv(DATA_DIR / "train.csv")

# Убираем ID
X = train_df.drop(columns=["medv", "ID"])
y = train_df["medv"]

# Разделение
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Обучение
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Оценка
y_pred = model.predict(X_valid)
rmse = mean_squared_error(y_valid, y_pred, squared=False)

print("RMSE:", rmse)

# Сохранение модели
joblib.dump(model, MODEL_DIR / "model.joblib")