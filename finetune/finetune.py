import os
import numpy as np
import pandas as pd
import mlflow

from copy import deepcopy
from sklearn.metrics import accuracy_score
from mlflow.tracking import MlflowClient
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


# Safely loads CSV file
def safe_load_csv(path):
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, header=None)
    return df if not df.empty else None


# Load train, test, and finetune datasets
def load_datasets():
    # Train
    df_train = pd.read_csv("data/train.csv", header=None)
    X_train, y_train = df_train.iloc[:, 0:4].to_numpy(), df_train.iloc[:, 4].to_numpy()

    # Test
    df_test = pd.read_csv("data/test.csv", header=None)
    X_test, y_test = df_test.iloc[:, 0:4].to_numpy(), df_test.iloc[:, 4].to_numpy()

    # Finetune
    df_ft = safe_load_csv("data/finetune.csv")
    if df_ft is not None:
        X_ft, y_ft = df_ft.iloc[:, 0:4].to_numpy(), df_ft.iloc[:, 4].to_numpy()
    else:
        X_ft, y_ft = np.empty((0, 4), dtype=np.float32), np.empty((0,), dtype=np.int64)

    return (X_train, y_train), (X_test, y_test), (X_ft, y_ft)


# Finetune the latest model from MLflow Model Registry
def finetune_model():
    # Setup MLflow
    mlflow.sklearn.autolog(silent=True)
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_URL", "http://localhost:5000"))
    mlflow.set_experiment("IrisDev-Finetune")

    # Load datasets
    (X_train, y_train), (X_test, y_test), (X_ft, y_ft) = load_datasets()

    # Load the latest sklearn model from MLflow Model Registry
    model = mlflow.sklearn.load_model("models:/IrisDev/latest")

    # Finetune parameters
    tuned = deepcopy(model)
    tuned.warm_start = True
    seed = 42
    tuned.random_state = seed

    # Raise iteration limit
    tuned.max_iter = getattr(model, "max_iter", 100) + 5
    # Lower learning rate
    lr_init = getattr(model, "learning_rate_init", 0.001)
    tuned.learning_rate_init = lr_init / 10.0

    # Concatenate train and finetune datasets
    X_concat = np.vstack([X_train, X_ft]) if X_ft.size else X_train
    y_concat = np.concatenate([y_train, y_ft]) if y_ft.size else y_train

    # Sample weights: train = 0.7, finetune = 1.0
    w_train = np.full(len(X_train), 0.7, dtype=np.float32)
    w_ft = np.full(len(X_ft), 1.0, dtype=np.float32)
    sample_weight = np.concatenate([w_train, w_ft]) if X_ft.size else w_train

    with mlflow.start_run() as run:
        # Train the model
        tuned.fit(X_concat, y_concat, sample_weight=sample_weight)

        # Test and log metrics
        y_pred = tuned.predict(X_test)
        test_acc = accuracy_score(y_test, y_pred)
        mlflow.log_metric("test_accuracy", float(test_acc))

        # Export and log the finetuned model in ONNX format
        initial_types = [('input', FloatTensorType([None, X_concat.shape[1]]))]
        onnx_model = convert_sklearn(tuned, initial_types=initial_types)
        mlflow.onnx.log_model(onnx_model, "onnx")

        # Register models if accuracy threshold is met
        client = MlflowClient()
        print(f"Finomhangolt teszt pontossága: {test_acc:.4f}")
        if test_acc >= 0.90:
            # Register sklearn model
            sklearn_src = f"runs:/{run.info.run_id}/model"
            mv1 = mlflow.register_model(sklearn_src, "IrisDev")
            print(f"Sklearn modell regisztrálva IrisDev néven, verzió: {mv1.version}")

            # Register ONNX model
            onnx_src = f"runs:/{run.info.run_id}/onnx"
            mv2 = mlflow.register_model(onnx_src, "IrisModel")
            print(f"ONNX modell regisztrálva IrisModel néven, verzió: {mv2.version}")
        else:
            print("Pontosság < 0.90, nem regisztrálunk új verziót.")
