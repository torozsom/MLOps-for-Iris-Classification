import mlflow
from mlflow.tracking import MlflowClient
import numpy as np
import onnxruntime as rt
import json
import os
import threading

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from prometheus_fastapi_instrumentator import Instrumentator
from typing import Callable
from prometheus_client import Info
from prometheus_client import Counter
import requests

state = {}


# Application settings
class Settings(BaseSettings):
    class_path: str = "data/classes.json"
    mlflow_uri: str = "http://localhost:5000"
    prefect_api_url: str = os.getenv("PREFECT_API_URL", "http://localhost:4200/api")


# Input model for the predict endpoint
class PredictInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# Output model for the predict endpoint
class PredictOutput(BaseModel):
    class_name: str


# Input model for the suggest endpoint
class SuggestInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    expected_class_name: str


# Response model for the suggest endpoint
class SuggestResponse(BaseModel):
    deployment_id: str
    flow_run_id: str | None = None
    parameters: dict


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield
    state.clear()


settings = Settings()


def predicted_class_name() -> Callable[[Info], None]:
    METRIC = Counter(
        "predicted_class_name",
        "Number of times a certain class predicted",
        labelnames=("class_name",)
    )

    def instrumentation(info: Info) -> None:
        if info.request.url.path == '/predict' and info.response.status_code == 200:
            class_name = json.loads(info.response.body)['class_name']
            METRIC.labels(class_name).inc()

    return instrumentation


app = FastAPI(lifespan=lifespan)
(Instrumentator(body_handlers=[r".*"])
 .instrument(app)
 .add(predicted_class_name())
 .expose(app)
 )


def init():
    # Configure MLflow tracking
    mlflow.set_tracking_uri(settings.mlflow_uri)

    # Initialize a lock for safe hot-reloads
    state['model_lock'] = threading.Lock()

    # Determine latest available version from MLflow Model Registry
    model_name = "IrisModel"
    client = MlflowClient(tracking_uri=settings.mlflow_uri)
    try:
        versions = client.search_model_versions(f"name='{model_name}'")
        latest_version = max(int(v.version) for v in versions) if versions else None
    except Exception:
        latest_version = None

    # Load the model (specific version if known, else 'latest')
    try:
        if latest_version is not None:
            model_uri = f"models:/{model_name}/{latest_version}"
            state['model_version'] = latest_version
        else:
            model_uri = f"models:/{model_name}/latest"
            state['model_version'] = None
        model = mlflow.onnx.load_model(model_uri)
    except Exception as e:
        # Surface a helpful error early
        raise RuntimeError(f"Failed to load ONNX model from MLflow at '{model_uri}': {e}")

    # Create ONNX Runtime session
    session = rt.InferenceSession(
        model.SerializeToString(),
        providers=["CPUExecutionProvider"]
    )
    state['session'] = session

    # Load class names
    class_names = None
    if os.path.exists(settings.class_path):
        with open(settings.class_path, 'r') as f:
            class_names = json.load(f)
    state['class_names'] = class_names


def _get_latest_model_version(model_name: str = "IrisModel") -> int | None:
    """Return the highest version number for the given registered model, or None if unavailable."""
    try:
        client = MlflowClient(tracking_uri=settings.mlflow_uri)
        versions = client.search_model_versions(f"name='{model_name}'")
        if not versions:
            return None
        return max(int(v.version) for v in versions)
    except Exception:
        return None


def _load_session_for_version(version: int | None, model_name: str = "IrisModel") -> rt.InferenceSession:
    """Load ONNX model by explicit version (or 'latest' if None) and return an ONNX Runtime session."""
    if version is None:
        model_uri = f"models:/{model_name}/latest"
    else:
        model_uri = f"models:/{model_name}/{version}"
    model = mlflow.onnx.load_model(model_uri)
    return rt.InferenceSession(model.SerializeToString(), providers=["CPUExecutionProvider"])


def maybe_update_model(model_name: str = "IrisModel") -> None:
    """If a newer model version exists in MLflow, hot-reload the ONNX session atomically."""
    latest = _get_latest_model_version(model_name)
    current = state.get('model_version')
    # If we cannot determine latest (None) but current is also None, nothing to do.
    if latest is None or latest == current:
        return
    # Reload under lock
    lock = state.get('model_lock')
    if lock is None:
        # Shouldn't happen, but load without lock if needed
        session = _load_session_for_version(latest, model_name)
        state['session'] = session
        state['model_version'] = latest
        return
    with lock:
        # Double-check inside lock
        if state.get('model_version') == latest:
            return
        session = _load_session_for_version(latest, model_name)
        state['session'] = session
        state['model_version'] = latest


@app.post("/predict")
async def predict(input: PredictInput) -> PredictOutput:
    # Check for a newer model version and hot-reload if needed
    maybe_update_model("IrisModel")

    # Create the input tensor
    input_tensor = np.array([[input.sepal_length, input.sepal_width, input.petal_length, input.petal_width]],
                            dtype=np.float32)

    # Predict the class
    input_name = state['session'].get_inputs()[0].name
    output_class, _ = state['session'].run(None, {input_name: input_tensor})

    # Determine the class name
    class_name = f"Class {output_class[0]}"
    if state['class_names'] is not None:
        class_name = state['class_names'][output_class[0]]

    return PredictOutput(class_name=class_name)


# Prefect client for interacting with the Prefect API
class PrefectClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or settings.prefect_api_url).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })

    def get_deployment(self, flow_name: str, deployment_name: str | None = None) -> dict:
        # Try the two-path variant first
        if deployment_name:
            url = f"{self.base_url}/deployments/name/{flow_name}/{deployment_name}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            # fall back to single-name variant
        url = f"{self.base_url}/deployments/name/{flow_name}"
        resp = self.session.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def create_flow_run(self, deployment_id: str, parameters: dict) -> dict:
        url = f"{self.base_url}/deployments/{deployment_id}/create_flow_run"
        resp = self.session.post(url, json={"parameters": parameters}, timeout=10)
        resp.raise_for_status()
        return resp.json()


# Suggest endpoint to trigger a Prefect flow run
@app.post("/suggest", response_model=SuggestResponse)
async def suggest(input: SuggestInput) -> SuggestResponse:
    client = PrefectClient()

    # Resolve deployment ID
    try:
        deployment = client.get_deployment(
            flow_name="Iris Finetune Ingest",
            deployment_name="iris-finetune-ingest",
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to resolve Prefect deployment: {e}")

    deployment_id = deployment.get("id") or deployment.get("deployment_id")
    if not deployment_id:
        raise HTTPException(status_code=500, detail="Deployment ID not found in Prefect response")

    params = {
        "sepal_length": input.sepal_length,
        "sepal_width": input.sepal_width,
        "petal_length": input.petal_length,
        "petal_width": input.petal_width,
        "expected_class_name": input.expected_class_name,
    }

    try:
        run_resp = client.create_flow_run(deployment_id, params)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to create Prefect flow run: {e}")

    flow_run_id = run_resp.get("id") or run_resp.get("flow_run_id")
    return SuggestResponse(deployment_id=deployment_id, flow_run_id=flow_run_id, parameters=params)
