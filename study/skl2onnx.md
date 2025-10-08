# skl2onnx: Converting scikit-learn Models to ONNX

skl2onnx converts trained scikit-learn models (and pipelines) into the ONNX format for portable, high-performance inference with runtimes like onnxruntime.

- Why convert to ONNX
- What ONNX is
- Supported models and operators
- Conversion workflow
- Initial types and shapes
- Dealing with preprocessing pipelines
- Validation and testing
- Tips and pitfalls
- How this project uses skl2onnx

---

## 1) Why Convert to ONNX?

- Portability: run the same model across languages and platforms.
- Performance: onnxruntime provides optimized kernels.
- Standardization: consistent deployment format across frameworks.

---

## 2) What Is ONNX?

- Open Neural Network Exchange format: a graph of typed operators.
- Framework-agnostic; many exporters/importers exist (PyTorch, TensorFlow, sklearn via skl2onnx).

---

## 3) Supported Models and Operators

- skl2onnx supports many sklearn estimators (linear models, trees, SVMs, MLP, etc.).
- The conversion maps sklearn steps to ONNX operators; some edge cases may need custom converters.

---

## 4) Conversion Workflow

- Train your sklearn model/pipeline.
- Determine input schema (feature count, dtypes) and create `initial_types` with ONNX types.
- Call `convert_sklearn(model, initial_types=...)` to obtain an ONNX model.
- Serialize with `model.SerializeToString()` or let MLflow log it via `mlflow.onnx.log_model`.

Example:
```python
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
onnx = convert_sklearn(model, initial_types=[('input', FloatTensorType([None, n_features]))])
```

---

## 5) Initial Types and Shapes

- Most tabular models expect a 2D float input of shape [N, n_features].
- Use `FloatTensorType([None, n_features])`; many sklearn models accept float32.
- Ensure your inference code feeds the same dtype (np.float32) and the right shape.

---

## 6) Preprocessing Pipelines

- Convert full sklearn Pipelines to preserve preprocessing steps in ONNX.
- When converting pipelines with encoders/scalers, ensure operators are supported; otherwise, split preprocessing outside the ONNX graph.

---

## 7) Validation and Testing

- Compare sklearn `predict`/`predict_proba` with onnxruntime outputs on a sample batch within tolerance.
- Keep the same preprocessing, feature order, and dtype.

---

## 8) Tips and Pitfalls

- Pitfall: dtype mismatch (float64 vs float32) — convert inputs to float32 for ONNX.
- Pitfall: unsupported operators — upgrade skl2onnx or simplify the pipeline.
- Include model metadata (class labels) outside ONNX if needed (e.g., `classes.json`).

---

## 9) How This Project Uses skl2onnx

- `main.py` converts trained `MLPClassifier` models to ONNX and logs them to MLflow.
- `finetune/finetune.py` converts the finetuned model to ONNX and logs it as well.
- The API loads the ONNX model from MLflow and runs inference with onnxruntime.
