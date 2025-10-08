# Pandas: Data Analysis with Python

Pandas is Python’s de facto library for tabular data. It provides DataFrame and Series structures for loading, transforming, aggregating, and saving structured datasets.

- What is Pandas and why use it
- Core data structures: Series and DataFrame
- Reading/writing data
- Indexing, selecting, filtering
- Transformations: apply, map, groupby
- Joining/merging and reshaping
- Handling missing data
- Performance tips
- Using Pandas in ML pipelines
- How this project uses Pandas

---

## 1) Why Pandas?

- Human-friendly API for tabular operations.
- Integrates with NumPy and scikit-learn.
- Essential for data cleaning, feature engineering, and EDA.

---

## 2) Data Structures

- Series: 1D labeled array.
- DataFrame: 2D labeled table with columns of potentially different types.

Create DataFrames:
- From CSV: `pd.read_csv("data.csv")`
- From dicts/lists: `pd.DataFrame({"a":[1,2],"b":[3,4]})`

---

## 3) I/O (Input/Output)

- CSV: `pd.read_csv`, `df.to_csv`
- Parquet: `pd.read_parquet`, `df.to_parquet`
- SQL: `pd.read_sql`, `to_sql`
- JSON/Excel and many more formats.

Choose column types with `dtype=`, handle headers with `header=`, and missing values with `na_values`.

---

## 4) Indexing and Selection

- Column selection: `df["col"]`, `df[["c1","c2"]]`
- Row selection by label: `df.loc[indexer]`
- Row selection by position: `df.iloc[pos]`
- Boolean filtering: `df[df["col"] > 0]`

---

## 5) Transformations

- Vectorized ops: `df["c"] = df["a"] + df["b"]`
- `apply` row/column-wise custom functions.
- `map`/`replace` for value mapping.
- `groupby` + `agg` for aggregations.

---

## 6) Joins and Reshaping

- `merge` for SQL-like joins on keys.
- `concat` to stack vertically/horizontally.
- `pivot`, `melt` to reshape long/wide.

---

## 7) Missing Data

- Detect: `df.isna().sum()`
- Fill: `df.fillna(value)` or strategies (mean/median/etc.).
- Drop: `df.dropna()`

---

## 8) Performance Tips

- Use categorical dtypes for low-cardinality strings.
- Prefer vectorized operations over Python loops.
- For very large data, consider chunked `read_csv(chunksize=...)` or switch to libraries like Polars/Dask.

---

## 9) Pandas in ML Pipelines

- Load and split datasets.
- Feature engineering (scaling, encoding) often via scikit-learn transformers.
- Convert to NumPy: `df.values`/`df.to_numpy()` for sklearn.

---

## 10) How This Project Uses Pandas

- Training and test sets are read via `pd.read_csv` in `main.py` and `finetune/finetune.py`.
- The Prefect flow appends to `finetune.csv` using Pandas to read/concat and save.
- Pandas enables simple yet reliable manipulation of tabular iris features and labels.
