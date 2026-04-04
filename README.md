# Boston Housing MLOps Project

## Description
MLOps project implementing a full machine learning lifecycle for regression task using Boston Housing dataset.

Target variable: `medv`  
Task type: regression  
Metric: RMSE  

---

## Technologies

- Python 3.12
- pandas, numpy
- scikit-learn
- FastAPI
- pydantic
- pytest
- DVC
- Docker, docker-compose
- GitHub Actions (CI/CD)

---

## Project Structure

```
Boston-Housing-MLOps/
├── app/                    # FastAPI application
│   └── main.py
├── src/                    # training and inference logic
│   ├── train.py
│   ├── predict.py
│   └── config.py
├── data/raw/               # datasets
├── models/                 # trained model artifact
├── tests/                  # unit tests
├── frontend/               # web UI (static files)
├── scripts/                # scenario runner
├── .github/workflows/      # CI/CD pipelines
├── config.ini              # configuration
├── dvc.yaml                # DVC pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Setup

```bash
conda activate boston-mlops-py312
pip install -r requirements.txt
```

---

## Training

```bash
python -m src.train
```

Result:
- model saved to `models/model.joblib`
- RMSE printed in console

---

## Batch Prediction

```bash
python -m src.predict
```

Result:
- `submission.csv` generated

---

## API

Run:

```bash
python -m uvicorn app.main:app --reload
```

Available endpoints:

- `GET /health`
- `GET /feature-metadata`
- `POST /predict`

Swagger:
```
http://127.0.0.1:8000/docs
```

---

## Frontend

Available at:
```
http://127.0.0.1:8000/
```

Features:
- input form for 13 features
- prediction display
- formatted output (e.g. `$31.84k`)

---

## Testing

```bash
pytest -v
```

Covers:
- training logic
- prediction logic
- API endpoints

---

## DVC

```bash
dvc repro
```

Tracks:
- model artifact
- metrics

---

## Docker

Build:

```bash
docker build -t boston-housing-api:latest .
```

Run:

```bash
docker compose up --build
```

Check:

```bash
curl http://127.0.0.1:8000/health
```

---

## CI/CD

### CI (GitHub Actions)

- install dependencies
- run tests
- build Docker image
- push image to DockerHub

### CD

- pull image from DockerHub
- run container
- wait for API readiness
- run scenario tests

---

## Scenario testing

```bash
python scripts/run_scenario.py
```

Validates:
- health endpoint
- metadata endpoint
- prediction endpoint
