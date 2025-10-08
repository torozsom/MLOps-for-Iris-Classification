# NumPy: The Foundation of Numerical Computing in Python

NumPy provides the N-dimensional array (ndarray) and vectorized operations that power scientific Python. Many libraries (Pandas, scikit-learn, SciPy) are built on it.

- Why NumPy
- ndarrays and dtypes
- Vectorized operations and broadcasting
- Indexing, slicing, boolean masking
- Linear algebra and random numbers
- Performance and memory layout
- Interoperability (Pandas, sklearn, ONNX)
- Tips and pitfalls
- How this project uses NumPy

---

## 1) Why NumPy?

- Efficient numerical arrays with contiguous memory for speed.
- Rich math functions and ufuncs written in C.
- Backbone of the PyData ecosystem.

---

## 2) ndarrays and dtypes

- Create arrays: `np.array`, `np.zeros`, `np.ones`, `np.arange`, `np.linspace`.
- Data types: float32/64, int32/64, bool, complex; pick types deliberately for performance/compatibility.

---

## 3) Vectorized Ops and Broadcasting

- Apply operations to entire arrays without Python loops (fast!).
- Broadcasting aligns shapes to perform element-wise operations.
- Example: `X * 2 + 1` or `X + y` where `y` is 1D broadcast across rows.

---

## 4) Indexing and Slicing

- `a[0, 1]`, `a[:, 0]`, `a[::2]` for strides and slices.
- Boolean masks: `a[a > 0.5]`.
- Fancy indexing with index arrays.

---

## 5) Linear Algebra and RNG

- `np.dot`, `@`, `np.linalg.inv`, `svd`, `eig` for linear algebra.
- Random numbers: `np.random.default_rng(seed).normal(...)`.

---

## 6) Performance and Memory

- Prefer contiguous arrays and vectorized code.
- Avoid copying unnecessarily; use views via slices.
- Be mindful of dtype to reduce memory footprint.

---

## 7) Interoperability

- Pandas stores columns as NumPy arrays under the hood.
- scikit-learn accepts NumPy arrays as inputs/outputs.
- ONNX models expect specific dtypes (often float32), so convert with `astype(np.float32)`.

---

## 8) Tips and Pitfalls

- Pitfall: silent dtype upcasting; check `a.dtype`.
- Pitfall: shape mismatches; inspect `a.shape`.
- Use `np.newaxis` or `[:, None]` to add dimensions for broadcasting.

---

## 9) How This Project Uses NumPy

- Convert DataFrames to NumPy arrays for training and prediction.
- Prepare ONNX input tensors with dtype float32 for onnxruntime inference in the API.
- Construct weights and concatenated matrices during fine-tuning.
