# FastAPI: Modern, Fast Web APIs with Python

FastAPI is a high-performance, developer-friendly web framework for building APIs in Python. It leverages type hints (Pydantic) for validation and automatic documentation.

- Why FastAPI
- Core concepts: path operations, request/response models
- Validation with Pydantic
- Dependency injection and settings
- Async support and performance
- Interactive docs (OpenAPI/Swagger, ReDoc)
- Middlewares and instrumentation
- Deploying FastAPI (uvicorn, gunicorn)
- How this project uses FastAPI

---

## 1) Why FastAPI?

- Speed: built on Starlette and Pydantic, with async support.
- Developer productivity: auto-generated docs, clear types, validation.
- Easy to integrate with ML inference code.

---

## 2) Core Concepts

- Path operations: `@app.get("/path")`, `@app.post("/predict")` map HTTP methods/paths to Python callables.
- Request/response models: Pydantic models define inputs and outputs with types.

Example:
```python
from fastapi import FastAPI
from pydantic import BaseModel

class PredictInput(BaseModel):
    x: float

class PredictOutput(BaseModel):
    y: float

app = FastAPI()

@app.post("/predict", response_model=PredictOutput)
def predict(inp: PredictInput) -> PredictOutput:
    return PredictOutput(y=inp.x * 2)
```

---

## 3) Validation with Pydantic

- Ensures inputs have the correct types and constraints.
- Generates clear error messages when validation fails.

---

## 4) Dependency Injection and Settings

- FastAPI provides `Depends` for injecting dependencies (DB connections, settings objects).
- Settings libraries (like `pydantic-settings`) load env vars cleanly.

---

## 5) Async Support and Performance

- Write `async def` endpoints for non-blocking IO (DB calls, HTTP requests).
- Use background tasks for non-critical work.

---

## 6) Docs

- Swagger UI at `/docs` and ReDoc at `/redoc` generated automatically from type hints and docstrings.

---

## 7) Middlewares and Instrumentation

- Add middlewares for CORS, auth, logging.
- Instrument endpoints with Prometheus exporters for metrics.

---

## 8) Deployment

- Run with uvicorn: `uvicorn main:app --host 0.0.0.0 --port 80`.
- In production, often behind a reverse proxy and using gunicorn workers with uvicorn workers for concurrency.

---

## 9) How This Project Uses FastAPI

- Exposes `/predict` to serve ONNX model predictions.
- Exposes `/suggest` to trigger a Prefect flow that appends finetune data and conditionally retrains.
- Loads settings via `pydantic-settings`, instruments endpoints with Prometheus, and hot-reloads the model version based on MLflow Model Registry.
