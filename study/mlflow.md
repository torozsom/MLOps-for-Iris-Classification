# MLflow: Experiment Tracking, Model Registry, and Deployment

MLflow is a platform to manage the ML lifecycle: experiment tracking, model packaging, and model registry. It integrates with many frameworks and supports pluggable storage and serving.

- Why MLflow
- Architecture: tracking server, backend store, artifact store, registry
- Tracking runs: parameters, metrics, artifacts
- Autologging
- Model registry and stages
- Model formats and flavors (sklearn, ONNX)
- Loading models in applications
- Integration with Docker, Prefect, and FastAPI
- Best practices
- How this project uses MLflow

---

## 1) Why MLflow?

- Central place to record experiments.
- Compare runs and find best models.
- Register and promote models across stages (Staging, Production).
- Standardize inference with model flavors.

---

## 2) Architecture

- Tracking Server: REST API + UI.
- Backend Store: stores run metadata (e.g., SQLite, MySQL, or the default file store). In Docker here, bundled in the image.
- Artifact Store: stores artifacts (models, plots); here, mounted to `mlflow_mlartifacts` volume.
- Model Registry: stores model names and versions with metadata.

---

## 3) Tracking Runs

- Start runs explicitly (`mlflow.start_run`) or rely on autologging.
- Log params: `mlflow.log_param`.
- Log metrics: `mlflow.log_metric`.
- Log artifacts: `mlflow.log_artifact` or model flavors (e.g., `mlflow.onnx.log_model`).

Autologging (e.g., `mlflow.sklearn.autolog`) automatically logs common items during fit.

---

## 4) Model Registry

- Register model versions from a run URI: `mlflow.register_model("runs:/<run_id>/model", "Name")`.
- Promote versions by stages, add descriptions and tags.
- Consumers (APIs) refer to `models:/Name/Version` or `models:/Name/Production`.

---

## 5) Model Flavors

- MLflow supports many: sklearn, PyTorch, TensorFlow, ONNX, etc.
- For ONNX: `mlflow.onnx.log_model(onnx_model, "onnx")`; later load with `mlflow.onnx.load_model("models:/IrisModel/latest")`.

---

## 6) Loading Models in Applications

- Use the right flavor’s loader (sklearn vs onnx).
- Your API loads ONNX models via MLflow, then creates an onnxruntime session.

---

## 7) Integration with Docker, Prefect, FastAPI

- Docker Compose runs the MLflow Tracking UI.
- Prefect tasks reference `MLFLOW_URL` to log finetune runs to the same server.
- FastAPI pulls the latest model from the Model Registry to serve predictions.

---

## 8) Best Practices

- Use experiments (`mlflow.set_experiment`) to group runs logically.
- Tag runs with data versions and code commit hashes.
- Store both framework-native and ONNX variants for portability.
- Use the Registry to control deployment rather than ad-hoc files.

---

## 9) How This Project Uses MLflow

- `main.py` autologs runs for hyperparameter sweeps and registers best models as `IrisDev` (sklearn) and `IrisModel` (ONNX).
- `finetune/finetune.py` logs finetuned runs and registers new versions when accuracy ≥ 0.90.
- `api/api.py` loads `IrisModel` by version or alias `latest` and hot-reloads newer versions on the fly.
