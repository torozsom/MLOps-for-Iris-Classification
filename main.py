import os
import pandas as pd
import numpy as np
import json
import mlflow

from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import log_loss, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


def main():
    # MLflow setup
    mlflow.sklearn.autolog(silent=True)
    mlflow.set_tracking_uri(os.getenv("MLFLOW_URL", "http://localhost:5000"))
    mlflow.set_experiment('IrisDev')

    # Reading data
    train_path = 'data/train.csv'
    df = pd.read_csv(train_path, header=None)
    X = df.iloc[:, 0:4]
    y = df.iloc[:, 4]

    # Load class names
    class_path = 'data/classes.json'
    with open(class_path, 'r') as f:
        class_names = json.load(f)

    # Train-validation split in 75:25 ratio
    seed = 42
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25, random_state=seed)

    # Hyperparameter tuning
    parameters = {
        'hidden_layers': [2, 3, 4],
        'epochs': [100, 250, 500, 750, 1000]
    }

    search_results = []

    for params in ParameterGrid(parameters):
        with mlflow.start_run() as run:
            model = MLPClassifier(
                hidden_layer_sizes=tuple(np.repeat(10, params['hidden_layers'])),
                max_iter=params['epochs'],
                random_state=seed
            )
            # Train model
            model.fit(X_train, y_train)

            # Validation loss calculation
            y_prob = model.predict_proba(X_val)
            loss = log_loss(y_val, y_prob)

            # ONNX export and log
            onnx = convert_sklearn(model, initial_types=[('input', FloatTensorType([None, X_train.shape[1]]))])
            mlflow.onnx.log_model(onnx, name='onnx')

            # Store results
            search_results.append((loss, params, model, run.info.run_id))

    # Choose best model based on minimum validation loss
    min_loss, best_params, best_model, best_run = min(search_results, key=lambda x: x[0])
    print(f"A legjobb modell vesztesége {min_loss:.4f}, paraméterei {best_params}")

    # Test evaluation
    test_path = 'data/test.csv'
    df_test = pd.read_csv(test_path, header=None)
    X_test = df_test.iloc[:, 0:4]
    y_test = df_test.iloc[:, 4]

    # Accuracy evaluation
    y_pred = best_model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print(f"Teszt pontosság: {test_acc * 100:.2f}%")

    # Show confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    disp.plot()
    plt.show()

    # Register and tag the best model
    tags = {
        'test_accuracy': float(test_acc),
        'epochs': best_params['epochs'],
        'hidden_layers': best_params['hidden_layers'],
    }
    mlflow.register_model(f'runs:/{best_run}/onnx', 'IrisModel', tags=tags)

    # ONNX export into file
    best_onnx = convert_sklearn(best_model, initial_types=[('input', FloatTensorType([None, X_train.shape[1]]))])
    model_path = "models/model.onnx"
    with open(model_path, "wb") as f:
        f.write(best_onnx.SerializeToString())

    # Register sklearn model
    mv = mlflow.register_model(f'runs:/{best_run}/model', 'IrisDev', tags=tags)
    print(f"Sklearn model 'IrisDev' regisztrálva, verzió: {mv.version}")


if __name__ == "__main__":
    main()
