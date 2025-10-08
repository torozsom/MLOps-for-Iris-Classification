# Prometheus: Monitoring and Metrics for Modern Systems

Prometheus is an open-source monitoring system and time-series database designed for reliability and scalability. It scrapes metrics, stores them with labels, and enables querying via PromQL.

- Why Prometheus
- Metrics model and labels
- Scraping and service discovery
- Exporters and client libraries
- PromQL basics
- Alerting and recording rules
- Integrations (Grafana, Kubernetes, FastAPI)
- How this project uses Prometheus

---

## 1) Why Prometheus?

- Pull-based scraping of metrics at regular intervals.
- Multi-dimensional data model with labels for powerful queries.
- Robust, simple architecture without external dependencies.

---

## 2) Metrics Model and Labels

- Time series identified by metric name and key-value labels.
- Types: counter, gauge, histogram, summary.
- Labels let you slice/dice metrics (e.g., by endpoint, status code, class name).

---

## 3) Scraping and Discovery

- Prometheus server scrapes HTTP endpoints that expose metrics (`/metrics`).
- Targets configured statically or discovered dynamically (Kubernetes, Consul, etc.).

---

## 4) Exporters and Client Libraries

- Exporters expose metrics for popular systems (node_exporter, postgres_exporter, etc.).
- Client libraries (Python, Go, Java) let applications publish custom metrics.

---

## 5) PromQL Basics

- Query current values: `http_requests_total`.
- Rates: `rate(http_requests_total[5m])`.
- Aggregations: `sum by (status)(rate(http_requests_total[1m]))`.
- Histograms: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`.

---

## 6) Alerting and Recording Rules

- Recording rules precompute queries to speed up dashboards.
- Alerting rules evaluate conditions and send alerts to Alertmanager.

---

## 7) Integrations

- Grafana visualizes Prometheus data with rich dashboards.
- In Python APIs, `prometheus_client` and wrappers like `prometheus-fastapi-instrumentator` expose metrics.

---

## 8) How This Project Uses Prometheus

- The API integrates `prometheus-fastapi-instrumentator` to expose standard HTTP metrics and a custom counter tracking predicted class names.
- `prometheus.yml` configures scrape jobs for the API and potentially for other services.
- Grafana (optional) can be used to plot latency, error rates, and the distribution of predictions in real time.
