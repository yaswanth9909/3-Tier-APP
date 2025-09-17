from fastapi import FastAPI, Request
import os, json, psycopg2, psycopg2.extras

app = FastAPI()
DB_DSN = os.getenv("POSTGRES_DSN", "postgresql://postgres:postgres@db:5432/postgres")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def db_health():
    try:
        conn = psycopg2.connect(DB_DSN)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close(); conn.close()
        return {"db": "ok"}
    except Exception as e:
        return {"db": "error", "detail": str(e)}

@app.get("/")
def home():
    return {"message": "Hello from Docker (compose)!"}

@app.post("/orders")
async def create_order(req: Request):
    data = await req.json()
    conn = psycopg2.connect(DB_DSN)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders(
          id SERIAL PRIMARY KEY,
          payload JSONB NOT NULL,
          created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("INSERT INTO orders(payload) VALUES (%s) RETURNING id, payload, created_at", [json.dumps(data)])
    row = cur.fetchone()
    conn.commit()
    cur.close(); conn.close()
    return {"inserted": row}
