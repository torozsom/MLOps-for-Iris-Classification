# scikit-learn (sklearn): Classic Machine Learning in Python

scikit-learn is a comprehensive library for classical machine learning, providing estimators for classification, regression, clustering, dimensionality reduction, model selection, and preprocessing.

- Why scikit-learn
- Estimator API: fit, predict, transform
- Pipelines and preprocessing
- Model selection: train/test split, cross-validation, grid search
- Metrics and evaluation
- Persisting models and interoperability (ONNX)
- Best practices
- How this project uses sklearn

---

## 1) Why scikit-learn?

- Consistent API across many algorithms.
- Strong documentation and community.
- Efficient implementations for small-to-medium datasets.
- Easy integration with Pandas/NumPy.

---

## 2) The Estimator API

- `fit(X, y)` trains a model.
- `predict(X)` returns predictions; `predict_proba(X)` for probabilistic classifiers.
- Transformers: `fit`, `transform`, and `fit_transform`.
- Pipelines chain transformers and estimators to avoid leakage.

---

## 3) Pipelines and Preprocessing

- Use `Pipeline` and `ColumnTransformer` for feature engineering (scaling, encoding) and to keep the same steps in train and inference.
- Example: `Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression())])`

---

## 4) Model Selection

- Split data: `train_test_split`.
- Cross-validation: `cross_val_score`, `StratifiedKFold`.
- Hyperparameter tuning: `GridSearchCV`, `RandomizedSearchCV`, `ParameterGrid`.

In this project, we sweep hidden layer sizes and epochs for an `MLPClassifier` and select the model with lowest validation loss.

---

## 5) Metrics and Evaluation

- Classification: accuracy, precision/recall/F1, ROC-AUC, confusion matrix.
- Regression: MSE/RMSE/MAE/R².
- Visualize with matplotlib/ConfusionMatrixDisplay.

---

## 6) Persisting Models and Interoperability

- Joblib/pickle for Python-native persistence.
- ONNX for portable, framework-agnostic inference. Convert via `skl2onnx` and run with `onnxruntime`.

---

## 7) Best Practices

- Fix random seeds for reproducibility (`random_state`).
- Use Pipelines to prevent data leakage.
- Evaluate with held-out test set.
- Track experiments (MLflow) and keep metadata.

---

## 8) How This Project Uses sklearn

- Train multiple MLPClassifier configurations; autolog runs to MLflow.
- Compute log loss and accuracy; show a confusion matrix.
- Convert best sklearn model to ONNX and register both sklearn and ONNX models to MLflow Model Registry for downstream serving.
- Fine-tuning continues training by lowering `learning_rate_init`, increasing `max_iter`, and using `warm_start`.
