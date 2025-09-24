from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os, json, time
import psycopg2, psycopg2.extras

# -----------------------------
# OpenTelemetry setup (tracing)
# -----------------------------
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Service name (helps identify traces in Grafana/Tempo)
SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "three-tier-api")

# Tempo endpoint (HTTP/OTLP). In-cluster FQDN for the Tempo service:
# The grafana/tempo Helm chart exposes OTLP HTTP on port 4318 by default.
OTLP_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://tempo.observability.svc.cluster.local:4318"
)

# Configure trace provider with resource attributes (service.name is important)
resource = Resource.create({"service.name": SERVICE_NAME})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Exporter will push spans to Tempo via OTLP/HTTP
otlp_exporter = OTLPSpanExporter(
    endpoint=f"{OTLP_ENDPOINT}/v1/traces",
)

# Batch processor = efficient export
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Create tracer (you can use it for custom spans)
tracer = trace.get_tracer(__name__)

# -----------------------------
# App & DB config
# -----------------------------
app = FastAPI()
DB_DSN = os.getenv("POSTGRES_DSN", "postgresql://postgres:postgres@db:5432/postgres")

# Auto-instrument FastAPI request handling
FastAPIInstrumentor.instrument_app(app)

# Auto-instrument psycopg2 DB calls
Psycopg2Instrumentor().instrument()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def db_health():
    try:
        with psycopg2.connect(DB_DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"db": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"db": "error", "detail": str(e)})

@app.get("/")
def home():
    return {"message": "Hello from Docker (Helm + OTEL)!"}

@app.post("/orders")
async def create_order(req: Request):
    # Example of a manual span around some “business logic”
    with tracer.start_as_current_span("create_order_handler"):
        data = await req.json()

        with psycopg2.connect(DB_DSN) as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            # Ensure table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders(
                  id SERIAL PRIMARY KEY,
                  payload JSONB NOT NULL,
                  created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            # Insert order
            cur.execute(
                "INSERT INTO orders(payload) VALUES (%s) RETURNING id, payload, created_at",
                [json.dumps(data)]
            )
            row = cur.fetchone()
            conn.commit()

        return {"inserted": row}
