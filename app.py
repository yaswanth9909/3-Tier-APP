# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg  # pip install "psycopg[binary]"

app = FastAPI()

DSN = os.getenv("POSTGRES_DSN", "postgresql://postgres:postgres@localhost:5432/postgres")

class OrderIn(BaseModel):
    item: str
    qty: int

@app.get("/")
def home():
    return {"ok": True, "msg": "hello"}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/health/db")
def health_db():
    try:
        with psycopg.connect(DSN, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"db error: {e}")

@app.post("/orders")
def create_order(order: OrderIn):
    try:
        with psycopg.connect(DSN, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS orders(
                        id SERIAL PRIMARY KEY,
                        item TEXT NOT NULL,
                        qty INT NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT now()
                    )
                """)
                cur.execute(
                    "INSERT INTO orders(item, qty) VALUES (%s, %s) RETURNING id",
                    (order.item, order.qty)
                )
                order_id = cur.fetchone()[0]
        return {"ok": True, "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"order insert failed: {e}")
