# Three-Tier Application (SRE Practice)

This repository contains a full **three-tier application** (Postgres + FastAPI + Nginx frontend) deployed across:
- Docker Compose (local dev)
- Kubernetes with Helm (kind/EKS)
- Terraform-provisioned EKS cluster (AWS)
- Observability stack (Prometheus, Loki, Tempo, Grafana)
- Data pipeline CronJob (summarizes orders into stats table)

---

##  Quick Start (Local with Docker Compose)

```bash
git clone https://github.com/<yaswanth9909>/<3-Tier-APP>.git
cd hellodocker
docker compose up -d --build
