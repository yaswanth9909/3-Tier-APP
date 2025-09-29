# Three-Tier Application

This repository contains a full three-tier application (Postgres + FastAPI + Nginx frontend) deployed across:

- Docker Compose (local dev)  
- Kubernetes with Helm (kind/EKS)  
- Terraform-provisioned EKS cluster (AWS)  
- Observability stack (Prometheus, Loki, Tempo, Grafana, Thanos)  
- Data pipeline CronJob (summarizes orders into stats table)  

---

## Quick Start (Local with Docker Compose)

```bash
git clone https://github.com/<yaswanth9909>/<3-tier-APP>.git
cd hellodocker
docker compose up -d --build
```
# Check the app

```bash
curl -s http://localhost:8080/health   # API health
curl -s http://localhost:8080/         # API root
curl -s -X POST http://localhost:8081/orders \
  -H "Content-Type: application/json" \
  -d '{"item":"pizza","qty":1}'
```

# Kubernetes with Helm (kind/EKS)

Install Helm chart

```bash
cd helm
helm upgrade --install three-tier ./three-tier -n three-tier --create-namespace
```

Check pods/services:

```bash
kubectl -n three-tier get pods
kubectl -n three-tier get svc
```
On EKS:
```bash
kubectl -n three-tier get svc frontend
```

# Obersevability Stack

Installed with Helm into observability namespace:

Prometheus → scrapes /metrics

Loki → central log storage

Tempo → distributed tracing

Grafana → dashboards (login admin / Admin123456789!)

Access Grafana

```bash
kubectl -n observability port-forward svc/prom-grafana 3000:80
```
# Data Pipeline

Cron job runs every minute

```bash
kubectl -n three-tier get cronjobs
kubectl -n three-tier get jobs
```
It summarizes orders into order_stats:

```bash
kubectl -n three-tier exec -it deploy/db -- \
  psql -U postgres -d postgres -c "SELECT * FROM order_stats ORDER BY ts DESC LIMIT 5;"
```

# CI/CD

GitHub Actions (.github/workflows/ci.yaml) runs on each push:

Builds and pushes Docker image to GHCR

Runs pytest on tests/test_app.py

Check CI status in Actions tab









