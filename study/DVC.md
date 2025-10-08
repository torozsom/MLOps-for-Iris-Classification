# DVC: Data Version Control for ML Projects

DVC (Data Version Control) brings Git-like workflows to large data, models, and pipelines. It helps you version datasets, track experiments, and define reproducible pipelines.

- Why DVC
- Core concepts: remotes, cache, locking, .dvc files, dvc.yaml
- Pipelines and stages
- Data versioning and storage
- Experiments and metrics
- DVC with MLflow
- Using DVC in containerized environments
- Best practices

---

## 1) Why DVC?

Git is great for code but not for large binary files. DVC lets you:
- Track large datasets and models without bloating your Git repo.
- Reproduce pipelines with `dvc.yaml` and `dvc.lock`.
- Share data via S3, GCS, Azure, SSH, local directories.
- Track metrics and plots per experiment.

---

## 2) Core Concepts

- .dvc files: small pointers in Git that reference large files stored in DVC cache.
- Cache: content-addressed storage on local disk or remote.
- Remotes: where the data lives (S3, GCS, SSH, etc.).
- dvc.yaml: defines pipeline stages, inputs, outputs, and params.
- dvc.lock: resolved, frozen snapshot of the pipeline with hashes for reproducibility.

---

## 3) Pipelines and Stages

A pipeline consists of stages:
- `cmd`: the command to run (e.g., `python preprocess.py`)
- `deps`: dependencies (code, params, data)
- `outs`: outputs (data artifacts)

DVC tracks hashes of deps/outs and re-runs stages only when inputs change.

---

## 4) Data Versioning and Storage

- Add large data files with `dvc add data/train.csv`—Git tracks the pointer, not the large file itself.
- Push/cache data to a remote with `dvc push` and share with collaborators who run `dvc pull`.
- Combine with branches/tags to associate data snapshots with code versions.

---

## 5) Experiments and Metrics

- DVC can track metrics (JSON/YAML/CSV) and plots (like learning curves).
- `dvc exp run` executes experiments with different params; `dvc exp show` compares outcomes.
- You can store metrics in files and declare them in `dvc.yaml` for auto-collection.

MLflow vs DVC experiments:
- MLflow excels at parameter/metric/artifact logging and registries.
- DVC complements with data versioning and pipeline definitions. Many teams use both.

---

## 6) DVC with MLflow

- Use DVC to ensure training data is versioned and recoverable.
- Use MLflow to track runs and models.
- Reference DVC dataset versions (git commit + dvc.lock) in MLflow run tags for auditability.

---

## 7) DVC in Containers

- Pipelines can be executed inside Docker for consistent environments.
- Mount credentials (cloud) securely for `dvc pull/push` in CI.
- Use `dvc repro` inside containers to rebuild artifacts from `dvc.yaml`.

---

## 8) Best Practices

- Keep data outside Git; commit only pointers and pipeline files.
- Use meaningful stage names in `dvc.yaml` and parameterize them.
- Store metrics/plots in structured files for automatic DVC collection.
- Align DVC stages with MLflow runs to correlate data and experiments.

---

## 9) Relation to This Repository

- The repo contains `dvc.yaml` and `dvc.lock`, suggesting stages for data preparation/training.
- You can integrate DVC stages around `preprocess.py` and `main.py` to reproduce datasets and models.
- Even if MLflow stores artifacts, DVC ensures the raw/processed data lineage is tracked, improving reproducibility and collaboration.
