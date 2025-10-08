# Docker: Containerization for Reproducible ML Systems

Docker is a platform to build, run, and share applications packaged with all their dependencies in lightweight containers. For MLOps, Docker ensures your training, serving, and orchestration tasks run consistently across laptops, CI, and production servers.

- Containers vs. virtual machines
- Images, layers, containers, registries
- Dockerfiles and best practices
- Docker Compose for multi-service apps
- Networking and volumes
- Using Docker for ML: training, serving, orchestration
- Security and performance considerations
- How this repository uses Docker

---

## 1) Containers vs. Virtual Machines

- VM: full OS virtualization; heavy; slow to boot.
- Container: process-level isolation; shares host kernel; lightweight and fast.
- Containers are ideal for microservices like API, MLflow UI, Prefect, and workers.

---

## 2) Core Concepts

- Image: immutable template (stack of layers) built from a Dockerfile.
- Layer: cached filesystem diff; enables fast rebuilds.
- Container: a running instance of an image.
- Registry: storage for images (Docker Hub, GHCR, ECR, etc.).

---

## 3) Dockerfile Essentials

- Base image: `FROM python:3.12`
- Working dir: `WORKDIR /code`
- Copy files: `COPY . .`
- Install deps: `RUN pip install -r requirements.txt`
- Entrypoint/CMD: what process should run by default.

Best practices:
- Keep images small: only install what you need.
- Leverage layer caching: copy and install requirements before app code.
- Pin versions to ensure reproducibility.
- Use non-root users where appropriate.

---

## 4) Docker Compose for Multi-Service Apps

Compose lets you define multi-container stacks: 
- Services: api, mlflow, prefect, finetune, prometheus, grafana
- Networks: automatic service discovery by name (e.g., `http://mlflow:5000`).
- Volumes: persist data (MLflow runs/artifacts; bind-mount `./data` for finetune).
- Dependencies: `depends_on` ensures startup order (not health).

Command examples:
- `docker compose build api finetune`
- `docker compose up -d mlflow prefect api finetune`
- `docker compose logs -f api`
- `docker compose down`

---

## 5) Networking and Volumes

- Each service is reachable by its Compose service name.
- Published ports map host to container (e.g., 80->80 for API, 5000->5000 for MLflow).
- Named volumes persist data between runs. Bind mounts sync local folders to containers.

In this project:
- MLflow persists to named volumes `mlflow_mlruns`, `mlflow_mlartifacts`.
- finetune service mounts `./data:/code/data` so feedback survives restarts.

---

## 6) Using Docker for ML

- Training images include compilers and science stacks.
- Serving images prioritize small size and fast startup (onnxruntime, FastAPI).
- Workers (Prefect) run flows that interact with MLflow and the filesystem.

Patterns:
- Separate build contexts per service (`api/Dockerfile`, `finetune/Dockerfile`).
- Configure services via environment variables (`MLFLOW_URL`, `PREFECT_API_URL`).

---

## 7) Security and Performance

- Limit container privileges; consider non-root users.
- Keep images patched and minimal.
- Use multi-stage builds to compile in one stage and copy artifacts to a slim runtime.
- Use CPU/GPU runtime as needed; onnxruntime has CPU and CUDA variants.

---

## 8) How This Repository Uses Docker

- `finetune/Dockerfile` builds a worker that serves a Prefect deployment and runs `finetune_flow.py`.
- `api/Dockerfile` (not shown here) builds the FastAPI server with onnxruntime and MLflow client.
- `docker-compose.yaml` wires together services: MLflow, Prefect, API, finetune worker, and optional Prometheus/Grafana.
- Environment variables connect services; volumes persist critical data.

Docker ensures that the system behaves the same across environments—crucial for reliable ML operations.
