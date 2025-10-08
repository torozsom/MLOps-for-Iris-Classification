# MLOps for Iris classification

---

## Project Overview

This is an end-to-end MLOps example for the Iris dataset:
- We train multiple scikit-learn MLP models and log them to MLflow.
- We export the best model to ONNX and register both sklearn and ONNX variants in MLflow’s Model Registry.
- A FastAPI service loads the ONNX model from MLflow and serves `/predict`.
- The same API exposes `/suggest` to collect user-labeled samples and trigger a Prefect flow.
- The Prefect flow appends samples to `data/finetune.csv` and, at a configurable threshold, runs fine-tuning and re-registers new model versions if quality is acceptable.
- The API automatically detects and hot-reloads the latest ONNX version from the Registry without restart.
- Prometheus scrapes API metrics; Grafana can visualize them.

---

## Python Components and Responsibilities

- `preprocess.py`
  - (If used) Prepare or validate source data into `data/train.csv`, `data/test.csv`, and `data/classes.json`.
  - Typical responsibilities: train/test split, normalization/encoding, data quality checks.

- `main.py`
  - Orchestrates experiment runs for MLPClassifier with different hyperparameters (hidden layers and epochs).
  - Uses Pandas to load data; NumPy for arrays.
  - Uses scikit-learn for training and metrics (accuracy, confusion matrix) and matplotlib for visualization.
  - Uses MLflow autologging to capture parameters, metrics, and artifacts.
  - Converts the best sklearn model to ONNX via `skl2onnx` and logs the ONNX artifact to MLflow.
  - Registers both models in the Model Registry:
    - `IrisDev` for the sklearn model (native flavor)
    - `IrisModel` for the ONNX model (ONNX flavor)

- `api/api.py`
  - FastAPI application with two main endpoints:
    - `POST /predict` receives four numeric inputs, runs the ONNX model via onnxruntime, and returns the predicted class name.
    - `POST /suggest` receives four numeric inputs + an expected class name, resolves the Prefect deployment ID, and triggers a new flow run via Prefect’s REST API.
  - Reads settings (MLFLOW URI, PREFECT API URL, classes path) via pydantic-settings.
  - Loads the ONNX model from MLflow Model Registry on startup (by explicit latest version if available) and creates an onnxruntime session.
  - Implements hot-reload: before every prediction, it checks MLflow for a newer `IrisModel` version and atomically swaps the session if a newer one exists.
  - Exposes Prometheus metrics via `prometheus-fastapi-instrumentator`, plus a custom counter for predicted class names.

- `finetune/finetune.py`
  - Loads training, test, and finetune datasets using Pandas and NumPy.
  - Loads the latest `IrisDev` sklearn model from MLflow.
  - Fine-tunes the model by increasing `max_iter`, reducing `learning_rate_init`, and enabling `warm_start`.
  - Trains on the concatenation of original training data and finetune data with sample weighting (train rows at 0.7, finetune rows at 1.0).
  - Evaluates on the test set, logs metrics to MLflow, converts to ONNX via `skl2onnx`, and logs the ONNX artifact.
  - If accuracy ≥ 0.90, registers new versions for both `IrisDev` and `IrisModel`.

- `finetune/finetune_flow.py`
  - Prefect flow that:
    - Accepts one new user sample and its expected class name.
    - Appends the sample as a new row to `data/finetune.csv`.
    - If the total row count is a multiple of `threshold` (default 5), runs `ft.finetune_model()`.
  - Is served as a Prefect deployment (`iris-finetune-ingest`) by the finetune worker container at startup.

---

## End-to-End Training and Registration

1. Run `main.py` to train multiple model configurations.
2. Autologging captures metrics/params/artifacts.
3. The best run’s sklearn model and ONNX artifact are registered as model versions in MLflow’s Model Registry.
4. MLflow’s UI (http://localhost:5000) lets you explore runs and model versions.

Key technologies: Pandas, NumPy, scikit-learn, matplotlib, skl2onnx, MLflow.

---

## Online Inference and Model Hot-Reload

- The API service starts, loads the latest `IrisModel` ONNX from MLflow, and builds an onnxruntime session.
- For each `/predict` request, the feature vector is turned into a float32 tensor and fed to onnxruntime; the corresponding class index is mapped to `classes.json`.
- Before running inference, the API checks for a newer model version and hot-reloads if found—no restarts required.

Key technologies: FastAPI, onnxruntime, MLflow, Prometheus.

---

## Feedback Ingestion and Fine-Tuning

- `/suggest` accepts labeled user samples and triggers the Prefect deployment.
- The Prefect flow appends the sample to `data/finetune.csv` and, at `threshold` count multiples, runs `finetune_model()`.
- The finetuning process logs a new MLflow run and may register newer model versions if the accuracy threshold is met.

Key technologies: Prefect, Pandas, NumPy, scikit-learn, MLflow, skl2onnx.

---

## Monitoring and Observability

- The API exposes Prometheus metrics; default HTTP metrics and a custom counter by predicted class name.
- Grafana (optional) can plot these metrics to monitor latency, error rates, and predictions distribution.
- MLflow UI provides experiment-level monitoring and model registry oversight.

Key technologies: Prometheus, Grafana, MLflow.

---

## How to Run the System Locally (Minimal Stack)

- Build and run the core services:
  - `docker compose build api finetune`
  - `docker compose up -d mlflow prefect finetune api`
- Seed the Model Registry once (if empty):
  - `$env:MLFLOW_URL = "http://localhost:5000"`
  - `python .\main.py`
- Interact:
  - Prefect UI: http://localhost:4200 (deployment `iris-finetune-ingest`)
  - MLflow UI: http://localhost:5000
  - API Docs: http://localhost/docs
- Test endpoints:
  - `POST /predict`: returns predicted class
  - `POST /suggest`: appends a user-labeled sample and triggers the Prefect flow

---

## Summary

- MLflow Registry provides a single source of truth for which model version to serve.
- ONNX + onnxruntime gives fast, portable inference independent of sklearn internals.
- FastAPI offers clean type-checked endpoints and auto docs.
- Prefect enables a clean, decoupled feedback loop and scheduled fine-tuning.
- Docker Compose provides reproducible multi-service infrastructure.
- Pandas/NumPy/sklearn deliver a clear baseline pipeline for tabular ML.
- Prometheus/Grafana ensure observability into API performance and usage patterns.
- MLflow UI provides a clean, visual experimentation experience.
