import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import psycopg

app = FastAPI()

# Use the same DSN you set in your Deployment env
DSN = os.getenv("POSTGRES_DSN", "postgresql://postgres:postgres@db:5432/postgres")

class OrderIn(BaseModel):
    item: str
    qty: int

@app.on_event("startup")
def ensure_schema():
    """Create a demo table if it doesn't exist."""
    try:
        with psycopg.connect(DSN, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS orders(
                        id SERIAL PRIMARY KEY,
                        item TEXT NOT NULL,
                        qty  INTEGER NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT now()
                    )
                """)
            # connection context commits automatically on success
    except Exception as e:
        # don't crash the app if DB is down; just log
        print("startup schema error:", e)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    try:
        with psycopg.connect(DSN, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e)})

@app.post("/orders")
def create_order(payload: OrderIn, request: Request):
    try:
        with psycopg.connect(DSN, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO orders(item, qty) VALUES (%s, %s) RETURNING id",
                    (payload.item, payload.qty),
                )
                new_id = cur.fetchone()[0]
        return {"id": new_id, "item": payload.item, "qty": payload.qty}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders")
def list_orders():
    try:
        with psycopg.connect(DSN, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, item, qty, created_at FROM orders ORDER BY id DESC LIMIT 50")
                rows = cur.fetchall()
        return [
            {"id": r[0], "item": r[1], "qty": r[2], "created_at": r[3].isoformat()}
            for r in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
