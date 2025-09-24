```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace observability
helm install prom prometheus-community/kube-prometheus-stack -n observability -f helm/values/kube-prom-values.yaml
helm install loki grafana/loki-stack -n observability -f helm/values/loki-values.yaml
helm install tempo grafana/tempo -n observability -f helm/values/tempo-values.yaml
