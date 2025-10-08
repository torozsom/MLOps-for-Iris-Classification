# Prefect: Orchestration for Data and ML Workflows

Prefect is a modern workflow orchestration system. It lets you define, schedule, and monitor data pipelines and ML tasks using Python-native workflows called flows and tasks.

- Why Prefect
- Core concepts: flows, tasks, deployments, work pools/queues
- Orchestration vs. execution
- Parameters and mapping
- Scheduling and triggering
- Observability (UI, logs, retries)
- Integrations with Docker, Kubernetes, and cloud
- Prefect vs. Airflow
- How this project uses Prefect

---

## 1) Why Prefect?

- Python-first, simple to author workflows.
- Hybrid execution: orchestrate from a central server while executing where you want.
- Great developer experience and observability.

---

## 2) Core Concepts

- Task: a Python callable wrapped with `@task`; has retries, caching, etc.
- Flow: a DAG of tasks, wrapped with `@flow`; entry point for orchestration.
- Deployment: a versioned, deployable config for a flow with parameters, schedules, and infra settings.
- Work Pool/Queue: how agents pick up scheduled runs for execution.

---

## 3) Orchestration vs. Execution

- Prefect Server/Cloud orchestrates runs: stores state, schedules, and results metadata.
- Agents/Workers execute tasks where you want (local, Docker, Kubernetes).

---

## 4) Parameters and Mapping

- Flows accept typed parameters; you can pass them on each run.
- Mapping lets you fan-out tasks across a collection of inputs.

---

## 5) Scheduling and Triggering

- Cron-like schedules or ad-hoc runs via API/UI.
- External systems (APIs) can trigger deployments by calling Prefect’s REST API.

---

## 6) Observability

- Prefect UI shows runs, logs, task states, retries, and artifacts.
- You can structure logs and emit metrics, and store results.

---

## 7) Integrations

- Run with Docker containers for reproducibility.
- Use blocks and collections for common infrastructure and secrets.

---

## 8) Prefect vs. Airflow

- Prefect: Pythonic, dynamic workflows, simpler local dev.
- Airflow: mature, strong scheduling, often more ops-heavy; DAGs are static.

Both are capable; choose based on team preferences and infra.

---

## 9) How This Project Uses Prefect

- Defines `finetune_ingest_flow` that appends a user-labeled sample to `data/finetune.csv` and, when a threshold is met, calls `ft.finetune_model()`.
- The finetune container serves a deployment (`iris-finetune-ingest`) to Prefect Server on startup.
- The API’s `/suggest` endpoint calls Prefect’s REST API to start a flow run with the input parameters.
- This implements an automated feedback loop: user feedback accumulates and periodically triggers model fine-tuning logged to MLflow.
