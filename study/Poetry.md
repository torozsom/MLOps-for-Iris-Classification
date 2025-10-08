# Poetry: Dependency Management and Packaging for Python

Poetry is a modern tool for managing Python project dependencies, virtual environments, and packaging. It aims to provide a single, consistent workflow for development to distribution.

- What is Poetry and why use it
- pyproject.toml and lock files
- Dependency resolution and version pinning
- Virtual environments
- Scripts, build, and publish
- Comparison to pip/venv/requirements.txt
- Using Poetry in ML/MLOps projects
- Practical tips and common pitfalls

---

## 1) What Is Poetry?

Poetry replaces ad-hoc combinations of pip, requirements.txt, and setup.py with a unified approach:
- Declare dependencies in `pyproject.toml`.
- Resolve compatible versions and lock them in `poetry.lock`.
- Manage virtual environments automatically.
- Build and publish packages.

Benefits:
- Reproducible environments via lock file.
- Cleaner project metadata and scripts in `pyproject.toml`.
- Consistent workflow across machines and CI/CD.

---

## 2) Key Files

- pyproject.toml: the single source of truth for your project’s metadata and dependencies. 
  - Example sections:
    - `[tool.poetry]`: name, version, authors
    - `[tool.poetry.dependencies]`: runtime deps
    - `[tool.poetry.group.dev.dependencies]`: dev/test deps
    - `[tool.poetry.scripts]`: CLI entry points
- poetry.lock: the exact versions resolved to ensure reproducibility.

---

## 3) Dependency Resolution and Pinning

- Poetry uses a solver to find a consistent set of dependency versions.
- Use semantic versioning ranges like `^1.3` or exact pins `==1.3.2`.
- `poetry update` refreshes lock; `poetry install` adheres to lock.

Why this matters in ML:
- Minor version differences can change results.
- Locking ensures experiments are reproducible.

---

## 4) Virtual Environments

- Poetry can create and manage a virtual environment per project.
- `poetry shell` to spawn a shell within venv; `poetry run python main.py` to run without activating.
- Configuration: `poetry config virtualenvs.in-project true` to create `.venv/` inside the repo.

---

## 5) Scripts, Build, and Publish

- Define CLI scripts in `pyproject.toml` under `[tool.poetry.scripts]`.
- Build wheels/sdists: `poetry build`.
- Publish to PyPI or internal index: `poetry publish`.

While this project primarily uses Docker for deployment, Poetry can still manage local dev deps and build artifacts that Docker layers install.

---

## 6) Poetry vs pip/requirements.txt

- requirements.txt is a flat list; Poetry models dependency graphs and metadata.
- Poetry lock file captures full resolution for reproducibility.
- Pip is ubiquitous and simple; Poetry adds structure and ergonomics.

In containerized prod, it’s common to export a deterministic requirements file from Poetry for smaller images:
- `poetry export -f requirements.txt --output requirements.txt --without-hashes`

---

## 7) Using Poetry in MLOps

- Pin versions for ML frameworks (scikit-learn, onnx, mlflow) to avoid surprises.
- Create groups for dev/test/lint (ruff, pytest) vs runtime.
- Combine with Docker: install dependencies via `poetry export` to a requirements.txt in the image.
- CI: `poetry install --no-root` for faster installs when you don’t need to build the package itself.

---

## 8) Practical Tips and Pitfalls

- Pitfall: Conflicting solver constraints. Solution: relax overly strict pins or align transitive deps.
- Pitfall: Different Python versions. Ensure `tool.poetry.dependencies.python = "^3.12"` (or your target) matches your runtime.
- Keep `poetry.lock` under version control.
- Use `poetry run` to avoid activating/deactivating venvs.

---

## 9) How It Relates to This Repository

- The project already has `pyproject.toml` and `poetry.lock`, which pin versions for reproducible dev.
- Docker images for runtime (API, finetune) install dependencies from `requirements.txt`—a common pattern where Poetry manages dev, and containers use frozen requirements at build time.
- If you expand the project, consider using Poetry groups for dev tools and exporting runtime requirements for the containers.
