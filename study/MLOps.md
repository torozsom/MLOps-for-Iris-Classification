# MLOps: A Complete Beginner-to-Advanced Guide

This guide is written for someone completely new to Machine Learning Operations (MLOps). We will start with the fundamentals and build up to concrete, practical workflows like the ones implemented in this repository (Iris classification project with training, fine-tuning, model registry, API serving, monitoring, and orchestration).

- What is MLOps and why it matters
- The ML lifecycle and where MLOps fits
- Core building blocks: data, code, models, experiments, CI/CD, deployment, monitoring
- Key tools you’ll see in this project: DVC, Poetry, Docker, Pandas/NumPy/sklearn, MLflow, skl2onnx/onnxruntime, FastAPI, Prometheus, Grafana, Prefect
- Environments and reproducibility
- Experiment tracking and model registry
- Deployment and serving patterns
- Monitoring and observability in production
- Orchestration and automation
- Typical pitfalls and best practices
- How all of this is used in this repo

---

## 1) What is MLOps?

MLOps (Machine Learning Operations) is the discipline of reliably and efficiently taking ML models from development (notebooks) into production (serving real users), and keeping them healthy throughout their lifecycle. It blends concepts from DevOps (automation, CI/CD, infra-as-code), Data Engineering (data pipelines, quality), and ML/DS (experiments, training, fine-tuning, evaluation).

Why MLOps matters:
- Reproducibility: Make sure you can rebuild a result later.
- Velocity: Iterate quickly while ensuring quality.
- Scalability: Serve models to users reliably.
- Governance: Track which data, code, and parameters produced a model.
- Maintainability: Update models safely when data drifts.

---

## 2) The ML Lifecycle

A simplified lifecycle:
1. Problem framing, data collection
2. Data preprocessing and feature engineering
3. Model training and hyperparameter tuning
4. Evaluation and selection
5. Packaging and deployment (batch or online)
6. Monitoring (performance, drift, cost)
7. Iteration: retraining/finetuning

MLOps provides the tooling and processes to automate and manage these steps.

---

## 3) Core Building Blocks

- Data: version, validate, and document datasets (e.g., with DVC). 
- Code: isolate dependencies (Poetry), version control (Git), test and lint.
- Models: train with frameworks (sklearn), export portability formats (ONNX).
- Experiments: track metrics, params, artifacts (MLflow).
- Registry: promote/baseline/best models (MLflow Model Registry).
- Serving: expose predictions via APIs (FastAPI) using efficient runtimes (onnxruntime).
- Orchestration: schedule flows (Prefect) for ingestion and finetuning.
- Monitoring: metrics and dashboards (Prometheus, Grafana).
- Containers: package runtime (Docker) for reproducibility everywhere.

---

## 4) Environments and Reproducibility

- Pin dependencies with Poetry or requirements.txt.
- Encapsulate runtime in Docker images.
- Capture data versions (DVC) and code commits (Git).
- Record experiments (MLflow) including parameters and artifacts.

In this project:
- Docker images run the API and finetuning worker.
- `mlflow` service persists runs and artifacts via named volumes.
- The `finetune` service mounts `./data` to persist incremental feedback.

---

## 5) Experiment Tracking and Model Registry (MLflow)

- Autolog experiments during training to record params, metrics, and artifacts.
- Convert sklearn models to ONNX and log both SKL and ONNX artifacts.
- Register best models to the Registry as versions (`IrisDev` for sklearn, `IrisModel` for ONNX).
- Use the Registry to control which version your API serves.

Benefits:
- Auditability: who trained what, when, with which data.
- Compare experiments and reproduce best runs.
- Controlled promotion to staging/production.

---

## 6) Model Packaging and Serving

- Why ONNX: framework-agnostic, optimized inference.
- Why onnxruntime: fast, portable CPU/GPU inference.
- Why FastAPI: modern, async, typed request/response models, easy docs.

Patterns:
- Pull model from MLflow Registry by name/version on startup.
- Hot-reload to newer versions without restart by periodically checking registry.
- Log metrics of usage (Prometheus) and visualize (Grafana).

---

## 7) Data and Feedback Loops

- Online feedback (e.g., user-labeled corrections) appended to a finetune dataset.
- Trigger finetuning when enough new samples are accumulated (threshold). 
- Orchestrate with Prefect: a flow appends data and conditionally launches finetune.
- Persist finetune.csv across container restarts via a bind mount.

---

## 8) Monitoring and Observability

- Export Prometheus metrics from the API (request count/latency, custom counters).
- Create Grafana dashboards for real-time overview.
- Watch model-level metrics via MLflow experiments.

What to monitor:
- Input distributions (drift), prediction distributions.
- Latency and error rate of endpoints.
- Data pipeline health and task success/failure (Prefect UI).

---

## 9) Orchestration (Prefect)

- Prefect provides flows (DAGs) and deployments for scheduling and ad-hoc runs.
- Your finetune flow appends one row per user input and triggers finetuning every N rows.
- The flow is served to Prefect Server from inside the `finetune` container.
- The API triggers the flow via Prefect REST when `/suggest` is called.

---

## 10) Typical Pitfalls and Best Practices

- Pitfall: Missing dependency at inference. Fix by pinning and testing Docker images (e.g., `onnxruntime`).
- Pitfall: Model registry empty. Seed initial model or code handles bootstrap.
- Use distinct names and explicit versions in MLflow.
- Keep environments minimal; rebuild images on dependency changes.
- Add end-to-end tests where possible (API + MLflow + Prefect integration test).

---

## 11) How This Repo Uses MLOps

- Training (`main.py`) uses MLflow autolog, hyperparameter sweep, ONNX export, and registers best models.
- API (`api/api.py`) serves ONNX from MLflow, auto-updates to newest version, exposes `/predict` and `/suggest`, and publishes Prometheus metrics.
- Finetuning (`finetune/finetune.py` and `finetune_flow.py`) appends feedback, triggers finetune at threshold, logs artifacts, and registers new versions if accuracy ≥ 0.90.
- Docker Compose wires services: mlflow, prefect, finetune worker, api; optional prometheus, grafana.

By studying these components, you gain a practical end-to-end blueprint for MLOps: from data and experiments to production serving, monitoring, and continuous improvement.
