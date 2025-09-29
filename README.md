Three-Tier Application (SRE Practice)

This repository contains a full three-tier application (Postgres + FastAPI + Nginx frontend) deployed across:

Docker Compose (local dev)

Kubernetes with Helm (kind/EKS)

Terraform-provisioned EKS cluster (AWS)

Observability stack (Prometheus, Loki, Tempo, Grafana, Thanos)

Data pipeline CronJob (summarizes orders into stats table)

Quick Start (Local with Docker Compose)
git clone https://github.com/<your-user>/<repo>.git
cd hellodocker
docker compose up -d --build

Check the app
curl -s http://localhost:8080/health   # API health
curl -s http://localhost:8080/         # API root
curl -s -X POST http://localhost:8081/orders \
  -H "Content-Type: application/json" \
  -d '{"item":"pizza","qty":1}'

Kubernetes with Helm (kind/EKS)

Install Helm chart:

cd helm
helm upgrade --install three-tier ./three-tier -n three-tier --create-namespace


Check pods/services:

kubectl -n three-tier get pods
kubectl -n three-tier get svc


If on EKS:

kubectl -n three-tier get svc frontend
# Grab the LoadBalancer DNS and open it in browser

📊 Observability Stack

Installed with Helm into observability namespace:

Prometheus → scrapes /metrics

Loki → central log storage

Tempo → distributed tracing

Grafana → dashboards (login admin / Admin123456!)

Access Grafana:

kubectl -n observability port-forward svc/grafana 3000:80

Data Pipeline (CronJob)

CronJob runs every minute:

kubectl -n three-tier get cronjobs
kubectl -n three-tier get jobs


It summarizes orders into order_stats:

kubectl -n three-tier exec -it deploy/db -- \
  psql -U postgres -d postgres -c "SELECT * FROM order_stats ORDER BY ts DESC LIMIT 5;"

CI/CD

GitHub Actions (.github/workflows/ci.yaml) runs on each push:

Builds and pushes Docker image to GHCR

Runs pytest on tests/test_app.py

Check CI status in Actions tab



