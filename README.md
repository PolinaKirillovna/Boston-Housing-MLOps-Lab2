# Boston Housing ML Project

## Описание проекта
Учебный MLOps-проект для предсказания стоимости жилья в пригородах Бостона по набору табличных признаков.

Целевая переменная: `medv`.

Проект развивается по классическому ML lifecycle:
- исследование данных в Google Colab;
- перенос логики в `.py`-скрипты;
- обучение и сохранение модели;
- API на FastAPI;
- далее: тесты, DVC, Docker, CI/CD.

## Датасет
Используется датасет **Boston Housing**.

Основные файлы данных:
- `data/raw/train.csv`
- `data/raw/test.csv`
- `data/raw/submission_example.csv`

## Модель
Текущая основная модель:
- `RandomForestRegressor`

На этапе исследования сравнивались:
- `LinearRegression` — baseline;
- `Ridge` — улучшенная линейная модель;
- `RandomForestRegressor` — нелинейная модель.

## Метрика
Основная метрика качества: **RMSE**.

Текущий результат локальной валидации:
- **RMSE ≈ 2.82**

## Структура проекта
```text
Boston-Housing-MLOps/
├── app/                 # FastAPI приложение
├── data/
│   ├── raw/             # исходные CSV-файлы
│   └── processed/       # подготовленные данные
├── models/              # сохранённые модели
├── notebooks/           # Colab / Jupyter ноутбуки
├── src/                 # обучение, предсказание, утилиты
├── tests/               # тесты
├── README.md
├── requirements.txt
└── .gitignore
```

## Требования к окружению
Рекомендуемый способ запуска:
- **macOS**
- **Anaconda Navigator**
- **PyCharm Community**
- отдельное `conda`-окружение

Текущая рабочая версия Python:
- **Python 3.12**

## Зависимости
Основные библиотеки проекта:
- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `seaborn`
- `fastapi`
- `uvicorn`
- `joblib`
- `pytest`
- `requests`

## Подготовка проекта
### 1. Создать conda environment
Через **Anaconda Navigator**:
- открыть вкладку **Environments**;
- создать окружение, например `boston-mlops-py312`;
- выбрать Python 3.12;
- установить необходимые библиотеки.

### 2. Открыть проект в PyCharm
- клонировать или открыть репозиторий;
- подключить созданное conda-окружение как Python Interpreter.

### 3. Положить данные
Файлы нужно разместить в папке:

```text
data/raw/
```

Ожидаемые файлы:
- `train.csv`
- `test.csv`
- `submission_example.csv`

## Как запускать проект
Все команды ниже выполняются **из корня проекта**.

### 1. Активировать окружение
```bash
conda activate boston-mlops-py312
```

### 2. Обучить модель
```bash
python src/train.py
```

Что делает команда:
- читает `data/raw/train.csv`;
- убирает `ID` из признаков;
- делит данные на train/validation;
- обучает `RandomForestRegressor`;
- считает RMSE;
- сохраняет модель в `models/model.joblib`.

Ожидаемый результат:
- в папке `models/` появляется файл `model.joblib`;
- в консоли выводится значение `Validation RMSE`.

### 3. Сформировать предсказания для test.csv
```bash
python src/predict.py
```

Что делает команда:
- загружает `models/model.joblib`;
- читает `data/raw/test.csv`;
- считает предсказания;
- формирует файл `submission.csv` в корне проекта.

### 4. Запустить API
```bash
python -m uvicorn app.main:app --reload
```

После запуска API будет доступен по адресу:
- `http://127.0.0.1:8000`

Swagger UI:
- `http://127.0.0.1:8000/docs`

## API
### GET /health
Проверка состояния сервиса.

Пример ответа:
```json
{
  "status": "ok",
  "model_exists": true
}
```

### POST /predict
Предсказание значения `medv` по признакам объекта недвижимости.

Пример запроса:
```json
{
  "crim": 0.02729,
  "zn": 0.0,
  "indus": 7.07,
  "chas": 0,
  "nox": 0.469,
  "rm": 7.185,
  "age": 61.1,
  "dis": 4.9671,
  "rad": 2,
  "tax": 242,
  "ptratio": 17.8,
  "black": 392.83,
  "lstat": 4.03
}
```

Пример ответа:
```json
{
  "predicted_medv": 31.8421
}
```

## Текущее состояние проекта
На текущем этапе уже реализовано:
- исследование данных в Colab;
- перенос логики обучения в `.py`;
- обучение модели и сохранение артефакта;
- генерация submission;
- FastAPI сервис;
- Swagger-документация.

Следующие этапы:
- тесты (`pytest`);
- DVC;
- Docker и docker-compose;
- CI/CD через GitHub Actions;
- фронтенд для взаимодействия с API.

## Примечания
- `ID` не используется как признак модели.
- Для линейных моделей scaling нужен, для `RandomForestRegressor` не обязателен.
- Проект специально развивается поэтапно, чтобы история коммитов отражала реальный процесс разработки.
