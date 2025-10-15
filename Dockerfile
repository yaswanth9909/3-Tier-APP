FROM python:3.11-slim

ENV PIP_DEFAULT_TIMEOUT=60 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# TLS + DNS sanity
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://tempo.observability.svc.cluster.local:4318 \
    OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
    OTEL_TRACES_SAMPLER=parentbased_always_on \
    OTEL_RESOURCE_ATTRIBUTES="service.name=api,deployment.environment=dev"

CMD ["opentelemetry-instrument","--traces_exporter","otlp","--metrics_exporter","none","--service_name","api","uvicorn","app:app","--host","0.0.0.0","--port","8000"]

