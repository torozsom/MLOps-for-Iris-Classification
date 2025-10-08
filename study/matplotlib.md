# Matplotlib: Plotting and Visualization in Python

Matplotlib is a comprehensive 2D plotting library for Python. It underpins many higher-level libraries (seaborn, pandas plotting) and provides fine-grained control over figures.

- Why Matplotlib
- Figure, Axes, and Artists
- Basic plots: line, scatter, bar, hist
- Styling: titles, labels, legends, themes
- Subplots and layouts
- Saving figures
- Interactive backends
- Tips for ML workflows
- How this project uses Matplotlib

---

## 1) Why Matplotlib?

- Mature, stable, and widely used.
- Full control for publication-quality figures.
- Integrates with NumPy and Pandas.

---

## 2) Figure, Axes, Artists

- Figure: the top-level container.
- Axes: the plotting area inside a figure (coordinate system).
- Artists: everything you see (lines, texts, patches).

Idioms:
- `fig, ax = plt.subplots()` creates a figure with one axes.
- `ax.plot(x, y)`, `ax.scatter(x, y)` add artists to axes.

---

## 3) Basic Plots

- Line: `ax.plot(x, y)`
- Scatter: `ax.scatter(x, y)`
- Bar: `ax.bar(categories, values)`
- Histogram: `ax.hist(data, bins=30)`

---

## 4) Styling

- Titles/labels: `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`
- Legend: `ax.legend()` with labels in plotting calls.
- Themes: `plt.style.use('ggplot')` or other styles.
- Colors/markers/linestyles specified via kwargs.

---

## 5) Subplots and Layouts

- `plt.subplots(nrows, ncols)` returns a grid of axes.
- Use `fig.tight_layout()` or `constrained_layout=True` to avoid overlap.

---

## 6) Saving Figures

- `plt.savefig('figure.png', dpi=150, bbox_inches='tight')`
- Save vector formats for print (`.svg`, `.pdf`) and raster for screens (`.png`).

---

## 7) Interactive Backends

- In notebooks, `%matplotlib inline` or `%matplotlib widget`.
- In scripts, `plt.show()` opens a window (if a GUI backend is available).

---

## 8) Tips for ML Workflows

- Plot learning curves, confusion matrices, feature importances.
- Use consistent styles and labels for comparability.
- Save artifacts to your experiment tracker (MLflow) for future reference.

---

## 9) How This Project Uses Matplotlib

- `main.py` renders a confusion matrix of predictions on the test set using `ConfusionMatrixDisplay` (built atop matplotlib). This helps visually assess which classes are confused by the model.
