# onnxruntime: High-Performance Inference for ONNX Models

onnxruntime is a cross-platform, high-performance scoring engine for Open Neural Network Exchange (ONNX) models. It supports CPU and GPU backends and a growing set of optimizations.

- Why onnxruntime
- Execution providers (CPU, CUDA, others)
- Sessions, inputs, and outputs
- Performance features (graph optimizations, IO binding)
- Precision and dtype considerations
- Integrations (MLflow, FastAPI)
- Troubleshooting
- How this project uses onnxruntime

---

## 1) Why onnxruntime?

- Fast inference with kernel-level optimizations.
- Portable across OSes and architectures.
- Supports many model types beyond deep learning (including classical ML exported to ONNX).

---

## 2) Execution Providers

- CPUExecutionProvider: default, optimized CPU kernels.
- CUDAExecutionProvider: GPU acceleration (requires proper CUDA/cuDNN stack and onnxruntime-gpu package).
- Others (DirectML on Windows, TensorRT, OpenVINO) available depending on platform and install.

Select providers when creating a session:
```python
import onnxruntime as rt
sess = rt.InferenceSession(onnx_bytes, providers=["CPUExecutionProvider"])  # or ["CUDAExecutionProvider"]
```

---

## 3) Sessions, Inputs, and Outputs

- Load model bytes or path into an `InferenceSession`.
- Inspect `session.get_inputs()` and `session.get_outputs()`.
- Run inference: `session.run(None, {input_name: input_tensor})` returns outputs.

Input tips:
- Ensure dtype and shape match the model (commonly float32, shape [N, features]).
- Name of the input must match the model graph input name; fetch it dynamically.

---

## 4) Performance Features

- Graph optimizations are enabled by default; can be tuned via session options.
- IO binding can help avoid copies for large arrays or GPU workflows.
- Batch multiple samples when possible to amortize overhead.

---

## 5) Precision and Dtypes

- Most ONNX tabular models expect float32.
- Mismatched dtypes cause runtime errors; always cast input tensors accordingly.

---

## 6) Integrations

- MLflow’s ONNX flavor returns an ONNX model object; you still create an onnxruntime session to run it.
- FastAPI can host an in-memory onnxruntime session and serve predictions at low latency.

---

## 7) Troubleshooting

- Import errors: ensure you installed `onnxruntime` (CPU) or `onnxruntime-gpu` (CUDA) compatible with your Python and CUDA versions.
- Shape or type mismatch: inspect `session.get_inputs()` and compare to your input array’s `dtype`/`shape`.
- Performance: verify execution providers and consider disabling debug builds.

---

## 8) How This Project Uses onnxruntime

- The API loads the ONNX artifact from MLflow and builds a `CPUExecutionProvider` session.
- It determines the input tensor name dynamically and runs `session.run(None, {name: tensor})`.
- The API supports hot-reloading to newer ONNX versions from the MLflow Model Registry without restarting.
